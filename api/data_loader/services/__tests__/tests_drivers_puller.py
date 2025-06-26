import unittest
from unittest.mock import Mock, patch, MagicMock
from django.test import TestCase

from data_loader.services.drivers_puller import DriversPuller
from teams.models import Team, Member, MemberRole, TeamStatus


class DriversPullerTest(TestCase):
    """Test cases for DriversPuller service"""

    def setUp(self):
        """Set up test data"""
        self.drivers_puller = DriversPuller()
        
        # Create a test team
        self.test_team = Team.objects.create(
            apisports_id=1,
            name='Red Bull Racing',
            description='Test team',
            status=TeamStatus.ACTIVE
        )
        
        # Mock API response data
        self.mock_driver_data = {
            'id': 1,
            'name': 'Max Verstappen',
            'number': 1,
            'abbr': 'VER',
            'country': {'code': 'NED'},
            'image': 'https://example.com/verstappen.jpg',
            'teams': [
                {
                    'team': {
                        'id': 1,
                        'name': 'Red Bull Racing'
                    }
                }
            ]
        }
        
        self.mock_rankings = [
            {'driver': {'id': 1}},
            {'driver': {'id': 2}}
        ]
        
        self.mock_drivers = [self.mock_driver_data]

    @patch('data_loader.services.drivers_puller.time.sleep')
    @patch.object(DriversPuller, '_process_driver')
    def test_pull_and_sync_drivers_success(self, mock_process_driver, mock_sleep):
        """Test successful drivers pulling and syncing"""
        with patch.object(self.drivers_puller.client, 'get_drivers_rankings') as mock_get_rankings, \
             patch.object(self.drivers_puller.client, 'get_driver') as mock_get_driver:
            
            mock_get_rankings.return_value = self.mock_rankings
            mock_get_driver.return_value = [self.mock_driver_data]
            
            result = self.drivers_puller.pull_and_sync_drivers()
            
            # Verify result
            self.assertTrue(result['success'])
            self.assertEqual(result['drivers_fetched'], 2)
            self.assertEqual(len(result['errors']), 0)
            
            # Verify API client methods were called
            mock_get_rankings.assert_called_once()
            self.assertEqual(mock_get_driver.call_count, 2)
            
            # Verify process_driver was called for each driver
            self.assertEqual(mock_process_driver.call_count, 2)

    @patch('data_loader.services.drivers_puller.time.sleep')
    def test_pull_and_sync_drivers_no_rankings(self, mock_sleep):
        """Test drivers pulling when no rankings are returned"""
        with patch.object(self.drivers_puller.client, 'get_drivers_rankings') as mock_get_rankings:
            mock_get_rankings.return_value = []
            
            result = self.drivers_puller.pull_and_sync_drivers()
            
            # Verify result
            self.assertFalse(result['success'])
            self.assertEqual(result['drivers_fetched'], 0)
            self.assertIn('No drivers found in APISports F1 API', result['errors'])

    @patch('data_loader.services.drivers_puller.time.sleep')
    def test_pull_and_sync_drivers_api_error(self, mock_sleep):
        """Test drivers pulling when API call fails"""
        with patch.object(self.drivers_puller.client, 'get_drivers_rankings') as mock_get_rankings:
            mock_get_rankings.side_effect = Exception('API connection failed')
            
            result = self.drivers_puller.pull_and_sync_drivers()
            
            # Verify result
            self.assertFalse(result['success'])
            self.assertEqual(result['drivers_fetched'], 0)
            self.assertIn('API connection failed', result['errors'])

    @patch('data_loader.services.drivers_puller.time.sleep')
    def test_pull_and_sync_drivers_driver_not_found(self, mock_sleep):
        """Test drivers pulling when individual driver is not found"""
        with patch.object(self.drivers_puller.client, 'get_drivers_rankings') as mock_get_rankings, \
             patch.object(self.drivers_puller.client, 'get_driver') as mock_get_driver:
            
            mock_get_rankings.return_value = self.mock_rankings
            mock_get_driver.return_value = []  # Empty driver data
            
            result = self.drivers_puller.pull_and_sync_drivers()
            
            # Should still succeed overall but have errors  
            self.assertTrue(result['success'])
            self.assertEqual(result['drivers_fetched'], 2)
            self.assertEqual(len(result['errors']), 2)  # Two driver not found errors

    @patch('data_loader.services.drivers_puller.time.sleep')
    @patch.object(DriversPuller, '_process_driver')
    def test_pull_and_sync_drivers_process_error(self, mock_process_driver, mock_sleep):
        """Test drivers pulling when processing individual driver fails"""
        mock_process_driver.side_effect = Exception('Processing error')
        
        with patch.object(self.drivers_puller.client, 'get_drivers_rankings') as mock_get_rankings, \
             patch.object(self.drivers_puller.client, 'get_driver') as mock_get_driver:
            
            mock_get_rankings.return_value = [{'driver': {'id': 1}}]
            mock_get_driver.return_value = [self.mock_driver_data]
            
            result = self.drivers_puller.pull_and_sync_drivers()
            
            # Should still succeed overall but have errors
            self.assertTrue(result['success'])
            self.assertEqual(result['drivers_fetched'], 1)
            self.assertIn('Error processing driver (1): Processing error', result['errors'])

    def test_process_driver_new_driver(self):
        """Test processing a new driver (creation)"""
        with patch.object(self.drivers_puller, '_find_driver') as mock_find_driver, \
             patch.object(self.drivers_puller, '_create_driver') as mock_create_driver:
            
            mock_find_driver.return_value = None  # Driver doesn't exist
            
            self.drivers_puller._process_driver(self.mock_driver_data)
            
            # Verify find_driver and create_driver were called
            mock_find_driver.assert_called_once_with(self.mock_driver_data)
            mock_create_driver.assert_called_once_with(self.mock_driver_data)
            
            # Verify result counters
            self.assertEqual(self.drivers_puller.result['drivers_created'], 1)
            self.assertEqual(self.drivers_puller.result['drivers_updated'], 0)

    def test_process_driver_existing_driver(self):
        """Test processing an existing driver (update)"""
        existing_driver = Member.objects.create(
            apisports_id=1,
            name='Max Verstappen',
            role=MemberRole.DRIVER,
            team=self.test_team
        )
        
        with patch.object(self.drivers_puller, '_find_driver') as mock_find_driver, \
             patch.object(self.drivers_puller, '_update_driver') as mock_update_driver:
            
            mock_find_driver.return_value = existing_driver
            
            self.drivers_puller._process_driver(self.mock_driver_data)
            
            # Verify find_driver and update_driver were called
            mock_find_driver.assert_called_once_with(self.mock_driver_data)
            mock_update_driver.assert_called_once_with(self.mock_driver_data, existing_driver)
            
            # Verify result counters
            self.assertEqual(self.drivers_puller.result['drivers_created'], 0)
            self.assertEqual(self.drivers_puller.result['drivers_updated'], 1)

    def test_create_driver(self):
        """Test driver creation"""
        with patch.object(self.drivers_puller, '_driver_params') as mock_driver_params:
            mock_params = {
                'name': 'Max Verstappen',
                'role': MemberRole.DRIVER,
                'team': self.test_team,
                'apisports_id': 1
            }
            mock_driver_params.return_value = mock_params
            
            self.drivers_puller._create_driver(self.mock_driver_data)
            
            # Verify driver_params was called
            mock_driver_params.assert_called_once_with(self.mock_driver_data)
            
            # Verify driver was created in database
            self.assertTrue(Member.objects.filter(name='Max Verstappen').exists())

    def test_update_driver(self):
        """Test driver update"""
        existing_driver = Member.objects.create(
            apisports_id=1,
            name='Old Name',
            role=MemberRole.DRIVER,
            team=self.test_team
        )
        
        with patch.object(self.drivers_puller, '_driver_params') as mock_driver_params:
            mock_params = {
                'name': 'Max Verstappen',
                'role': MemberRole.DRIVER,
                'team': self.test_team,
                'driver_number': 1
            }
            mock_driver_params.return_value = mock_params
            
            self.drivers_puller._update_driver(self.mock_driver_data, existing_driver)
            
            # Verify driver_params was called
            mock_driver_params.assert_called_once_with(self.mock_driver_data)
            
            # Verify driver was updated
            existing_driver.refresh_from_db()
            self.assertEqual(existing_driver.name, 'Max Verstappen')
            self.assertEqual(existing_driver.driver_number, 1)

    def test_driver_params(self):
        """Test driver parameters extraction from API data"""
        with patch.object(self.drivers_puller, '_find_team') as mock_find_team:
            mock_find_team.return_value = self.test_team
            
            params = self.drivers_puller._driver_params(self.mock_driver_data)
            
            expected_params = {
                'apisports_id': 1,
                'name': 'Max Verstappen',
                'description': 'F1 Driver - Max Verstappen',
                'role': MemberRole.DRIVER,
                'team': self.test_team,
                'driver_number': 1,
                'name_acronym': 'VER',
                'country_code': 'NED',
                'headshot_url': 'https://example.com/verstappen.jpg',
            }
            
            self.assertEqual(params, expected_params)

    def test_driver_params_no_team(self):
        """Test driver parameters extraction when no team data"""
        driver_data_no_team = {
            'id': 1,
            'name': 'Max Verstappen',
            'number': 1,
            'abbr': 'VER',
            'country': {'code': 'NED'},
            'image': 'https://example.com/verstappen.jpg',
            # Missing 'teams' key entirely
        }
        
        # Should work without teams (team will be None)
        params = self.drivers_puller._driver_params(driver_data_no_team)
        
        self.assertEqual(params['team'], None)
        self.assertEqual(params['name'], 'Max Verstappen')

    def test_driver_params_team_not_found(self):
        """Test driver parameters extraction when team is not found in database"""
        with patch.object(self.drivers_puller, '_find_team') as mock_find_team:
            mock_find_team.return_value = None  # Team not found
            
            with self.assertRaises(Exception) as context:
                self.drivers_puller._driver_params(self.mock_driver_data)
            
            self.assertIn('Could not find team for driver Max Verstappen', str(context.exception))

    def test_find_driver_by_apisports_id(self):
        """Test finding driver by API Sports ID"""
        driver = Member.objects.create(
            apisports_id=1,
            name='Max Verstappen',
            role=MemberRole.DRIVER,
            team=self.test_team
        )
        
        found_driver = self.drivers_puller._find_driver({
            'id': 1, 
            'name': 'Different Name', 
            'number': 999
        })
        
        self.assertEqual(found_driver, driver)

    def test_find_driver_by_name(self):
        """Test finding driver by name when API ID doesn't match"""
        driver = Member.objects.create(
            apisports_id=999,  # Different API ID
            name='Max Verstappen',
            role=MemberRole.DRIVER,
            team=self.test_team
        )
        
        found_driver = self.drivers_puller._find_driver({
            'id': 1, 
            'name': 'Max Verstappen', 
            'number': 1
        })
        
        self.assertEqual(found_driver, driver)

    def test_find_driver_by_number(self):
        """Test finding driver by driver number"""
        driver = Member.objects.create(
            apisports_id=999,  # Different API ID
            name='Different Name',  # Different name
            driver_number=1,
            role=MemberRole.DRIVER,
            team=self.test_team
        )
        
        found_driver = self.drivers_puller._find_driver({
            'id': 1, 
            'name': 'Max Verstappen', 
            'number': 1
        })
        
        self.assertEqual(found_driver, driver)

    def test_find_driver_not_found(self):
        """Test finding driver when it doesn't exist"""
        # Clear any existing drivers to ensure clean test
        Member.objects.filter(role=MemberRole.DRIVER).delete()
        
        found_driver = self.drivers_puller._find_driver({
            'id': 999, 
            'name': 'Non-existent Driver', 
            'number': 999
        })
        
        self.assertIsNone(found_driver)

    def test_find_team_by_apisports_id(self):
        """Test finding team by API Sports ID"""
        found_team = self.drivers_puller._find_team({'id': 1, 'name': 'Different Name'})
        
        self.assertEqual(found_team, self.test_team)

    def test_find_team_by_name(self):
        """Test finding team by name when API ID doesn't match"""
        # Clear any existing teams to ensure clean test
        Team.objects.all().delete()
        
        team = Team.objects.create(
            apisports_id=999,  # Different API ID
            name='Mercedes AMG',  # Different name to avoid conflicts
            description='Test team',
            status=TeamStatus.ACTIVE
        )
        
        found_team = self.drivers_puller._find_team({'id': 1, 'name': 'Mercedes AMG'})
        
        self.assertEqual(found_team, team)

    def test_find_team_not_found(self):
        """Test finding team when it doesn't exist"""
        found_team = self.drivers_puller._find_team({'id': 999, 'name': 'Non-existent Team'})
        
        self.assertIsNone(found_team)

    def test_initialization(self):
        """Test DriversPuller initialization"""
        puller = DriversPuller()
        
        # Verify client is initialized
        self.assertIsNotNone(puller.client)
        
        # Verify result structure is correct
        expected_result_keys = {
            'success', 'drivers_fetched', 'drivers_created', 
            'drivers_updated', 'errors'
        }
        self.assertEqual(set(puller.result.keys()), expected_result_keys)
        
        # Verify initial values
        self.assertFalse(puller.result['success'])
        self.assertEqual(puller.result['drivers_fetched'], 0)
        self.assertEqual(puller.result['drivers_created'], 0)
        self.assertEqual(puller.result['drivers_updated'], 0)
        self.assertEqual(puller.result['errors'], [])


if __name__ == '__main__':
    unittest.main() 