import unittest
from unittest.mock import Mock, patch, MagicMock
from django.test import TestCase
from datetime import datetime

from data_loader.services.races_puller import RacesPuller
from races.models import Race, Circuit, RaceStatus, Position
from teams.models import Team, Member, MemberRole, TeamStatus


class RacesPullerTest(TestCase):
    """Test cases for RacesPuller service"""

    def setUp(self):
        """Set up test data"""
        self.races_puller = RacesPuller()
        
        # Create test data
        self.test_circuit = Circuit.objects.create(
            name='Circuit de Monaco',
            location='Monaco'
        )
        
        self.test_team = Team.objects.create(
            apisports_id=1,
            name='Red Bull Racing',
            description='Test team',
            status=TeamStatus.ACTIVE
        )
        
        self.test_driver = Member.objects.create(
            apisports_id=1,
            name='Max Verstappen',
            role=MemberRole.DRIVER,
            team=self.test_team,
            driver_number=1
        )
        
        # Mock API response data
        self.mock_race_data = {
            'id': 1,
            'season': 2024,
            'type': 'Race',
            'status': 'completed',
            'distance': '260.286 km',
            'laps': {'total': 78},
            'fastest_lap': {'time': '1:12.909'},
            'competition': {
                'name': 'Monaco Grand Prix',
                'location': {
                    'country': 'Monaco',
                    'city': 'Monaco'
                }
            },
            'circuit': {
                'name': 'Circuit de Monaco'
            },
            'date': '2024-05-26T13:00:00Z'
        }
        
        self.mock_position_data = {
            'driver': {
                'id': 1,
                'name': 'Max Verstappen'
            },
            'position': 1,
            'points': 25,
            'laps': 78,
            'time': '1:41:06.982',
            'grid': '1',
            'pits': 2
        }

    @patch.object(RacesPuller, '_process_race')
    def test_pull_and_sync_races_success(self, mock_process_race):
        """Test successful races pulling and syncing"""
        mock_races = [self.mock_race_data]
        
        with patch.object(self.races_puller.client, 'get_races') as mock_get_races:
            mock_get_races.return_value = mock_races
            
            result = self.races_puller.pull_and_sync_races(2024)
            
            # Verify result
            self.assertTrue(result['success'])
            self.assertEqual(len(result['errors']), 0)
            
            # Verify API client was called with correct season
            mock_get_races.assert_called_once_with(2024)
            
            # Verify process_race was called for each race
            mock_process_race.assert_called_once_with(self.mock_race_data)

    @patch.object(RacesPuller, '_process_race')
    def test_pull_and_sync_races_default_season(self, mock_process_race):
        """Test races pulling with default season (current year)"""
        mock_races = [self.mock_race_data]
        
        with patch.object(self.races_puller.client, 'get_races') as mock_get_races, \
             patch('data_loader.services.races_puller.datetime') as mock_datetime:
            
            mock_datetime.now.return_value.year = 2024
            mock_get_races.return_value = mock_races
            
            result = self.races_puller.pull_and_sync_races()
            
            # Verify result
            self.assertTrue(result['success'])
            
            # Verify API client was called with current year
            mock_get_races.assert_called_once_with(2024)

    def test_pull_and_sync_races_api_error(self):
        """Test races pulling when API call fails"""
        with patch.object(self.races_puller.client, 'get_races') as mock_get_races:
            mock_get_races.side_effect = Exception('API connection failed')
            
            result = self.races_puller.pull_and_sync_races(2024)
            
            # Verify result
            self.assertFalse(result['success'])
            self.assertIn('API connection failed', result['errors'])

    @patch.object(RacesPuller, '_process_race')
    def test_pull_and_sync_races_process_error(self, mock_process_race):
        """Test races pulling when processing individual race fails"""
        mock_process_race.side_effect = Exception('Processing error')
        mock_races = [self.mock_race_data]
        
        with patch.object(self.races_puller.client, 'get_races') as mock_get_races:
            mock_get_races.return_value = mock_races
            
            result = self.races_puller.pull_and_sync_races(2024)
            
            # Should still succeed overall but have errors
            self.assertTrue(result['success'])
            self.assertIn('Error processing race: Processing error', result['errors'])

    @patch.object(RacesPuller, '_process_race_positions')
    @patch.object(RacesPuller, '_get_or_create_circuit')
    @patch.object(RacesPuller, '_find_race')
    @patch.object(RacesPuller, '_create_race')
    def test_process_race_new_race(self, mock_create_race, mock_find_race, 
                                  mock_get_or_create_circuit, mock_process_positions):
        """Test processing a new race (creation)"""
        mock_get_or_create_circuit.return_value = self.test_circuit
        mock_find_race.return_value = None  # Race doesn't exist
        mock_create_race.return_value = Mock(id='test-race-id')
        
        self.races_puller._process_race(self.mock_race_data)
        
        # Verify methods were called
        mock_get_or_create_circuit.assert_called_once_with(self.mock_race_data)
        mock_find_race.assert_called_once_with(self.mock_race_data)
        mock_create_race.assert_called_once()
        mock_process_positions.assert_called_once()
        
        # Verify result counters
        self.assertEqual(self.races_puller.result['races_created'], 1)
        self.assertEqual(self.races_puller.result['races_updated'], 0)

    @patch.object(RacesPuller, '_process_race_positions')
    @patch.object(RacesPuller, '_get_or_create_circuit')
    @patch.object(RacesPuller, '_find_race')
    @patch.object(RacesPuller, '_update_race')
    def test_process_race_existing_race(self, mock_update_race, mock_find_race, 
                                       mock_get_or_create_circuit, mock_process_positions):
        """Test processing an existing race (update)"""
        existing_race = Race.objects.create(
            apisports_id=1,
            circuit=self.test_circuit,
            name='Monaco Grand Prix',
            description='Test race',
            start_at=datetime.now(),
            status=RaceStatus.SCHEDULED
        )
        
        mock_get_or_create_circuit.return_value = self.test_circuit
        mock_find_race.return_value = existing_race
        mock_update_race.return_value = existing_race
        
        self.races_puller._process_race(self.mock_race_data)
        
        # Verify methods were called
        mock_get_or_create_circuit.assert_called_once_with(self.mock_race_data)
        mock_find_race.assert_called_once_with(self.mock_race_data)
        mock_update_race.assert_called_once()
        mock_process_positions.assert_called_once()
        
        # Verify result counters
        self.assertEqual(self.races_puller.result['races_created'], 0)
        self.assertEqual(self.races_puller.result['races_updated'], 1)

    def test_process_race_no_id(self):
        """Test processing race without API ID raises exception"""
        race_data_no_id = self.mock_race_data.copy()
        del race_data_no_id['id']
        
        with self.assertRaises(Exception) as context:
            self.races_puller._process_race(race_data_no_id)
        
        self.assertIn('has no API ID', str(context.exception))

    @patch.object(RacesPuller, '_find_circuit')
    @patch.object(RacesPuller, '_create_circuit')
    def test_get_or_create_circuit_new_circuit(self, mock_create_circuit, mock_find_circuit):
        """Test getting or creating a new circuit"""
        mock_find_circuit.return_value = None  # Circuit doesn't exist
        mock_create_circuit.return_value = self.test_circuit
        
        result = self.races_puller._get_or_create_circuit(self.mock_race_data)
        
        self.assertEqual(result, self.test_circuit)
        mock_find_circuit.assert_called_once()
        mock_create_circuit.assert_called_once()
        self.assertEqual(self.races_puller.result['circuits_created'], 1)

    @patch.object(RacesPuller, '_find_circuit')
    @patch.object(RacesPuller, '_update_circuit')
    def test_get_or_create_circuit_existing_circuit(self, mock_update_circuit, mock_find_circuit):
        """Test getting or creating an existing circuit"""
        mock_find_circuit.return_value = self.test_circuit
        mock_update_circuit.return_value = self.test_circuit
        
        result = self.races_puller._get_or_create_circuit(self.mock_race_data)
        
        self.assertEqual(result, self.test_circuit)
        mock_find_circuit.assert_called_once()
        mock_update_circuit.assert_called_once()
        self.assertEqual(self.races_puller.result['circuits_updated'], 1)

    def test_find_circuit_by_name(self):
        """Test finding circuit by name"""
        found_circuit = self.races_puller._find_circuit('Circuit de Monaco', 'Monaco')
        
        self.assertEqual(found_circuit, self.test_circuit)

    def test_find_circuit_by_location(self):
        """Test finding circuit by location"""
        circuit = Circuit.objects.create(
            name='Different Name',
            location='Monaco'
        )
        
        found_circuit = self.races_puller._find_circuit('Circuit de Monaco', 'Monaco')
        
        # Should find the first circuit with matching location
        self.assertIn(found_circuit, [self.test_circuit, circuit])

    def test_find_circuit_not_found(self):
        """Test finding circuit when it doesn't exist"""
        found_circuit = self.races_puller._find_circuit('Non-existent Circuit', 'Non-existent Location')
        
        self.assertIsNone(found_circuit)

    def test_create_circuit(self):
        """Test circuit creation"""
        circuit = self.races_puller._create_circuit('New Circuit', 'New Location')
        
        self.assertIsInstance(circuit, Circuit)
        self.assertEqual(circuit.name, 'New Circuit')
        self.assertEqual(circuit.location, 'New Location')

    def test_update_circuit(self):
        """Test circuit update"""
        updated_circuit = self.races_puller._update_circuit(
            self.test_circuit, 
            'Updated Circuit Name', 
            'Updated Location'
        )
        
        self.test_circuit.refresh_from_db()
        self.assertEqual(self.test_circuit.name, 'Updated Circuit Name')
        self.assertEqual(self.test_circuit.location, 'Updated Location')

    def test_find_race_by_apisports_id(self):
        """Test finding race by API Sports ID"""
        race = Race.objects.create(
            apisports_id=1,
            circuit=self.test_circuit,
            name='Monaco Grand Prix',
            description='Test race',
            start_at=datetime.now(),
            status=RaceStatus.SCHEDULED
        )
        
        found_race = self.races_puller._find_race({'id': 1, 'competition': {'name': 'Different Name'}})
        
        self.assertEqual(found_race, race)

    def test_find_race_not_found(self):
        """Test finding race when it doesn't exist"""
        found_race = self.races_puller._find_race({'id': 999, 'competition': {'name': 'Non-existent Race'}})
        
        self.assertIsNone(found_race)

    def test_create_race(self):
        """Test race creation"""
        with patch.object(self.races_puller, '_race_params') as mock_race_params:
            mock_params = {
                'apisports_id': 1,
                'circuit': self.test_circuit,
                'name': 'Monaco Grand Prix',
                'description': 'Test race',
                'start_at': datetime.now(),
                'status': RaceStatus.COMPLETED
            }
            mock_race_params.return_value = mock_params
            
            race = self.races_puller._create_race(self.mock_race_data, self.test_circuit)
            
            mock_race_params.assert_called_once_with(self.mock_race_data, self.test_circuit)
            self.assertIsInstance(race, Race)
            self.assertEqual(race.name, 'Monaco Grand Prix')

    def test_update_race(self):
        """Test race update"""
        existing_race = Race.objects.create(
            apisports_id=1,
            circuit=self.test_circuit,
            name='Old Name',
            description='Old description',
            start_at=datetime.now(),
            status=RaceStatus.SCHEDULED
        )
        
        with patch.object(self.races_puller, '_race_params') as mock_race_params:
            mock_params = {
                'name': 'Monaco Grand Prix',
                'status': RaceStatus.COMPLETED,
                'description': 'Updated description'
            }
            mock_race_params.return_value = mock_params
            
            updated_race = self.races_puller._update_race(
                existing_race, 
                self.mock_race_data, 
                self.test_circuit
            )
            
            existing_race.refresh_from_db()
            self.assertEqual(existing_race.name, 'Monaco Grand Prix')
            self.assertEqual(existing_race.status, RaceStatus.COMPLETED)

    def test_race_params(self):
        """Test race parameters extraction from API data"""
        with patch('data_loader.services.races_puller.parse_datetime') as mock_parse_datetime:
            mock_parse_datetime.return_value = datetime(2024, 5, 26, 13, 0, 0)
            
            params = self.races_puller._race_params(self.mock_race_data, self.test_circuit)
            
            expected_description = "Season: 2024 | Type: Race | Distance: 260.286 km | Total Laps: 78 | Fastest Lap: 1:12.909"
            
            self.assertEqual(params['apisports_id'], 1)
            self.assertEqual(params['circuit'], self.test_circuit)
            self.assertEqual(params['name'], 'Monaco Grand Prix')
            self.assertEqual(params['description'], expected_description)
            self.assertEqual(params['status'], RaceStatus.COMPLETED)

    def test_race_params_status_mapping(self):
        """Test race status mapping from API data"""
        test_cases = [
            ('completed', RaceStatus.COMPLETED),
            ('finished', RaceStatus.COMPLETED),
            ('ongoing', RaceStatus.ONGOING),
            ('live', RaceStatus.ONGOING),
            ('scheduled', RaceStatus.SCHEDULED),
            ('cancelled', RaceStatus.CANCELLED),
            ('canceled', RaceStatus.CANCELLED),
            ('unknown', RaceStatus.SCHEDULED)  # Default
        ]
        
        for api_status, expected_status in test_cases:
            race_data = self.mock_race_data.copy()
            race_data['status'] = api_status
            
            with patch('data_loader.services.races_puller.parse_datetime') as mock_parse_datetime:
                mock_parse_datetime.return_value = datetime.now()
                
                params = self.races_puller._race_params(race_data, self.test_circuit)
                self.assertEqual(params['status'], expected_status)

    @patch('data_loader.services.races_puller.time.sleep')
    @patch.object(RacesPuller, '_process_position')
    def test_process_race_positions_success(self, mock_process_position, mock_sleep):
        """Test processing race positions successfully"""
        mock_positions = [self.mock_position_data]
        
        race = Race.objects.create(
            apisports_id=1,
            circuit=self.test_circuit,
            name='Monaco Grand Prix',
            description='Test race',
            start_at=datetime.now(),
            status=RaceStatus.COMPLETED
        )
        
        with patch.object(self.races_puller.client, 'get_race_rankings') as mock_get_positions:
            mock_get_positions.return_value = mock_positions
            
            self.races_puller._process_race_positions(race, 1)
            
            mock_get_positions.assert_called_once_with(1)
            mock_process_position.assert_called_once_with(race, self.mock_position_data)
            mock_sleep.assert_called_once_with(10)

    @patch('data_loader.services.races_puller.time.sleep')
    @patch.object(RacesPuller, '_process_position')
    def test_process_race_positions_api_error(self, mock_process_position, mock_sleep):
        """Test processing race positions when API call fails"""
        race = Race.objects.create(
            apisports_id=1,
            circuit=self.test_circuit,
            name='Monaco Grand Prix',
            description='Test race',
            start_at=datetime.now(),
            status=RaceStatus.COMPLETED
        )
        
        with patch.object(self.races_puller.client, 'get_race_rankings') as mock_get_positions:
            mock_get_positions.side_effect = Exception('API error')
            
            # Should raise exception (method re-raises after logging)
            with self.assertRaises(Exception) as context:
                self.races_puller._process_race_positions(race, 1)
            
            self.assertEqual(str(context.exception), 'API error')
            mock_get_positions.assert_called_once_with(1)
            mock_process_position.assert_not_called()
            mock_sleep.assert_called_once_with(10)

    def test_process_position_new_position(self):
        """Test processing a new position (creation)"""
        race = Race.objects.create(
            apisports_id=1,
            circuit=self.test_circuit,
            name='Monaco Grand Prix',
            description='Test race',
            start_at=datetime.now(),
            status=RaceStatus.COMPLETED
        )
        
        with patch.object(self.races_puller, '_find_driver') as mock_find_driver, \
             patch.object(self.races_puller, '_find_position') as mock_find_position, \
             patch.object(self.races_puller, '_create_position') as mock_create_position:
            
            mock_find_driver.return_value = self.test_driver
            mock_find_position.return_value = None  # Position doesn't exist
            
            self.races_puller._process_position(race, self.mock_position_data)
            
            mock_find_driver.assert_called_once_with(self.mock_position_data)
            mock_find_position.assert_called_once_with(race, self.test_driver)
            mock_create_position.assert_called_once_with(race, self.test_driver, self.mock_position_data)
            
            self.assertEqual(self.races_puller.result['positions_created'], 1)

    def test_process_position_existing_position(self):
        """Test processing an existing position (update)"""
        race = Race.objects.create(
            apisports_id=1,
            circuit=self.test_circuit,
            name='Monaco Grand Prix',
            description='Test race',
            start_at=datetime.now(),
            status=RaceStatus.COMPLETED
        )
        
        existing_position = Position.objects.create(
            race=race,
            driver=self.test_driver,
            position=1,
            points=25
        )
        
        with patch.object(self.races_puller, '_find_driver') as mock_find_driver, \
             patch.object(self.races_puller, '_find_position') as mock_find_position, \
             patch.object(self.races_puller, '_update_position') as mock_update_position:
            
            mock_find_driver.return_value = self.test_driver
            mock_find_position.return_value = existing_position
            
            self.races_puller._process_position(race, self.mock_position_data)
            
            mock_find_driver.assert_called_once_with(self.mock_position_data)
            mock_find_position.assert_called_once_with(race, self.test_driver)
            mock_update_position.assert_called_once_with(existing_position, race, self.test_driver, self.mock_position_data)
            
            self.assertEqual(self.races_puller.result['positions_updated'], 1)

    def test_process_position_driver_not_found(self):
        """Test processing position when driver is not found"""
        race = Race.objects.create(
            apisports_id=1,
            circuit=self.test_circuit,
            name='Monaco Grand Prix',
            description='Test race',
            start_at=datetime.now(),
            status=RaceStatus.COMPLETED
        )
        
        with patch.object(self.races_puller, '_find_driver') as mock_find_driver:
            mock_find_driver.return_value = None  # Driver not found
            
            # Should not raise exception, just log error
            self.races_puller._process_position(race, self.mock_position_data)
            
            mock_find_driver.assert_called_once_with(self.mock_position_data)

    def test_find_driver_by_apisports_id(self):
        """Test finding driver by API Sports ID"""
        found_driver = self.races_puller._find_driver({'driver': {'id': 1, 'name': 'Different Name'}})
        
        self.assertEqual(found_driver, self.test_driver)

    def test_find_driver_by_name(self):
        """Test finding driver by name when API ID doesn't match"""
        # Clear any existing drivers to ensure clean test
        Member.objects.filter(role=MemberRole.DRIVER).delete()
        
        driver = Member.objects.create(
            apisports_id=999,  # Different API ID
            name='Lewis Hamilton',  # Different name to avoid conflicts
            role=MemberRole.DRIVER,
            team=self.test_team
        )
        
        found_driver = self.races_puller._find_driver({'driver': {'id': 1, 'name': 'Lewis Hamilton'}})
        
        self.assertEqual(found_driver, driver)

    def test_find_driver_not_found(self):
        """Test finding driver when it doesn't exist"""
        # Clear any existing drivers to ensure clean test
        Member.objects.filter(role=MemberRole.DRIVER).delete()
        
        found_driver = self.races_puller._find_driver({'driver': {'id': 999, 'name': 'Non-existent Driver', 'abbr': 'XXX', 'number': 999}})
        
        self.assertIsNone(found_driver)

    def test_initialization(self):
        """Test RacesPuller initialization"""
        puller = RacesPuller()
        
        # Verify client is initialized
        self.assertIsNotNone(puller.client)
        
        # Verify result structure is correct
        expected_result_keys = {
            'success', 'races_fetched', 'races_created', 'races_updated',
            'circuits_created', 'circuits_updated', 'positions_created', 
            'positions_updated', 'errors'
        }
        self.assertEqual(set(puller.result.keys()), expected_result_keys)
        
        # Verify initial values
        self.assertFalse(puller.result['success'])
        for key in expected_result_keys:
            if key == 'errors':
                self.assertEqual(puller.result[key], [])
            elif key != 'success':
                self.assertEqual(puller.result[key], 0)


if __name__ == '__main__':
    unittest.main() 