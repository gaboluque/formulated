import unittest
from unittest.mock import Mock, patch, MagicMock
from django.test import TestCase

from data_loader.services.teams_puller import TeamsPuller
from teams.models import Team, TeamStatus


class TeamsPullerTest(TestCase):
    """Test cases for TeamsPuller service"""

    def setUp(self):
        """Set up test data"""
        self.teams_puller = TeamsPuller()
        
        # Mock API response data
        self.mock_team_data = {
            'id': 1,
            'name': 'Red Bull Racing',
            'logo': 'https://example.com/redbull-logo.png',
            'base': 'Milton Keynes, United Kingdom',
            'first_team_entry': 2005,
            'world_championships': 5,
            'highest_race_finish': {'position': 1},
            'pole_positions': 75,
            'fastest_laps': 65,
            'president': 'Christian Horner',
            'director': 'Helmut Marko',
            'technical_manager': 'Adrian Newey',
            'chassis': 'RB19',
            'engine': 'Honda RBPT',
            'tyres': 'Pirelli'
        }
        
        self.mock_api_teams = [
            self.mock_team_data,
            {
                'id': 2,
                'name': 'Mercedes',
                'logo': 'https://example.com/mercedes-logo.png',
                'base': 'Brackley, United Kingdom',
                'first_team_entry': 2010,
                'world_championships': 8,
                'highest_race_finish': {'position': 1},
                'pole_positions': 128,
                'fastest_laps': 85,
                'president': 'Toto Wolff',
                'director': 'James Allison',
                'technical_manager': 'Mike Elliott',
                'chassis': 'W14',
                'engine': 'Mercedes',
                'tyres': 'Pirelli'
            }
        ]

    @patch('data_loader.services.teams_puller.time.sleep')
    @patch.object(TeamsPuller, '_process_team')
    def test_pull_and_sync_teams_success(self, mock_process_team, mock_sleep):
        """Test successful teams pulling and syncing"""
        # Mock the API client
        with patch.object(self.teams_puller.client, 'get_teams') as mock_get_teams:
            mock_get_teams.return_value = self.mock_api_teams
            
            result = self.teams_puller.pull_and_sync_teams()
            
            # Verify result
            self.assertTrue(result['success'])
            self.assertEqual(result['teams_fetched'], 2)
            self.assertEqual(len(result['errors']), 0)
            
            # Verify API client was called
            mock_get_teams.assert_called_once()
            
            # Verify process_team was called for each team
            self.assertEqual(mock_process_team.call_count, 2)
            mock_process_team.assert_any_call(self.mock_api_teams[0])
            mock_process_team.assert_any_call(self.mock_api_teams[1])

    @patch('data_loader.services.teams_puller.time.sleep')
    def test_pull_and_sync_teams_api_error(self, mock_sleep):
        """Test teams pulling when API call fails"""
        with patch.object(self.teams_puller.client, 'get_teams') as mock_get_teams:
            mock_get_teams.side_effect = Exception('API connection failed')
            
            result = self.teams_puller.pull_and_sync_teams()
            
            # Verify result
            self.assertFalse(result['success'])
            self.assertEqual(result['teams_fetched'], 0)
            self.assertIn('API connection failed', result['errors'])

    @patch('data_loader.services.teams_puller.time.sleep')
    @patch.object(TeamsPuller, '_process_team')
    def test_pull_and_sync_teams_process_error(self, mock_process_team, mock_sleep):
        """Test teams pulling when processing individual team fails"""
        # Mock process_team to raise exception for first team
        mock_process_team.side_effect = [Exception('Processing error'), None]
        
        with patch.object(self.teams_puller.client, 'get_teams') as mock_get_teams:
            mock_get_teams.return_value = self.mock_api_teams
            
            result = self.teams_puller.pull_and_sync_teams()
            
            # Should fail because processing error will be re-raised
            self.assertFalse(result['success'])
            self.assertEqual(result['teams_fetched'], 2)
            self.assertIn('Processing error', result['errors'])

    def test_process_team_new_team(self):
        """Test processing a new team (creation)"""
        with patch.object(self.teams_puller, '_find_team') as mock_find_team, \
             patch.object(self.teams_puller, '_create_team') as mock_create_team:
            
            mock_find_team.return_value = None  # Team doesn't exist
            
            self.teams_puller._process_team(self.mock_team_data)
            
            # Verify find_team and create_team were called
            mock_find_team.assert_called_once_with(self.mock_team_data)
            mock_create_team.assert_called_once_with(self.mock_team_data)
            
            # Verify result counters
            self.assertEqual(self.teams_puller.result['teams_created'], 1)
            self.assertEqual(self.teams_puller.result['teams_updated'], 0)

    def test_process_team_existing_team(self):
        """Test processing an existing team (update)"""
        existing_team = Team.objects.create(
            name='Red Bull Racing',
            description='Existing team',
            status=TeamStatus.ACTIVE
        )
        
        with patch.object(self.teams_puller, '_find_team') as mock_find_team, \
             patch.object(self.teams_puller, '_update_team') as mock_update_team:
            
            mock_find_team.return_value = existing_team
            
            self.teams_puller._process_team(self.mock_team_data)
            
            # Verify find_team and update_team were called
            mock_find_team.assert_called_once_with(self.mock_team_data)
            mock_update_team.assert_called_once_with(self.mock_team_data, existing_team)
            
            # Verify result counters
            self.assertEqual(self.teams_puller.result['teams_created'], 0)
            self.assertEqual(self.teams_puller.result['teams_updated'], 1)

    def test_create_team(self):
        """Test team creation"""
        with patch.object(self.teams_puller, '_team_params') as mock_team_params:
            mock_params = {
                'name': 'Red Bull Racing', 
                'status': TeamStatus.ACTIVE,
                'apisports_id': 1
            }
            mock_team_params.return_value = mock_params
            
            self.teams_puller._create_team(self.mock_team_data)
            
            # Verify team_params was called
            mock_team_params.assert_called_once_with(self.mock_team_data)
            
            # Verify team was created in database
            self.assertTrue(Team.objects.filter(name='Red Bull Racing').exists())
            
            # Verify counter incremented
            self.assertEqual(self.teams_puller.result['teams_created'], 1)

    def test_update_team(self):
        """Test team update"""
        existing_team = Team.objects.create(
            name='Old Name',
            description='Old description',
            status=TeamStatus.INACTIVE
        )
        
        with patch.object(self.teams_puller, '_team_params') as mock_team_params:
            mock_params = {
                'name': 'Red Bull Racing',
                'status': TeamStatus.ACTIVE,
                'apisports_id': 1
            }
            mock_team_params.return_value = mock_params
            
            self.teams_puller._update_team(self.mock_team_data, existing_team)
            
            # Verify team_params was called
            mock_team_params.assert_called_once_with(self.mock_team_data)
            
            # Verify team was updated
            existing_team.refresh_from_db()
            self.assertEqual(existing_team.name, 'Red Bull Racing')
            self.assertEqual(existing_team.status, TeamStatus.ACTIVE)
            self.assertEqual(existing_team.apisports_id, 1)

    def test_team_params(self):
        """Test team parameters extraction from API data"""
        params = self.teams_puller._team_params(self.mock_team_data)
        
        expected_params = {
            'apisports_id': 1,
            'name': 'Red Bull Racing',
            'description': 'Formula 1 Team - Red Bull Racing',
            'logo_url': 'https://example.com/redbull-logo.png',
            'base': 'Milton Keynes, United Kingdom',
            'first_team_entry': 2005,
            'world_championships': 5,
            'highest_race_finish': 1,
            'pole_positions': 75,
            'fastest_laps': 65,
            'president': 'Christian Horner',
            'director': 'Helmut Marko',
            'technical_manager': 'Adrian Newey',
            'chassis': 'RB19',
            'engine': 'Honda RBPT',
            'tyres': 'Pirelli',
            'status': TeamStatus.ACTIVE,
        }
        
        self.assertEqual(params, expected_params)

    def test_find_team_by_apisports_id(self):
        """Test finding team by API Sports ID"""
        team = Team.objects.create(
            apisports_id=1,
            name='Red Bull Racing',
            description='Test team',
            status=TeamStatus.ACTIVE
        )
        
        found_team = self.teams_puller._find_team({'id': 1, 'name': 'Different Name'})
        
        self.assertEqual(found_team, team)

    def test_find_team_by_name(self):
        """Test finding team by name when API ID doesn't match"""
        team = Team.objects.create(
            apisports_id=999,  # Different API ID
            name='Red Bull Racing',
            description='Test team',
            status=TeamStatus.ACTIVE
        )
        
        found_team = self.teams_puller._find_team({'id': 1, 'name': 'Red Bull Racing'})
        
        self.assertEqual(found_team, team)

    def test_find_team_not_found(self):
        """Test finding team when it doesn't exist"""
        found_team = self.teams_puller._find_team({'id': 999, 'name': 'Non-existent Team'})
        
        self.assertIsNone(found_team)

    def test_find_team_multiple_matches(self):
        """Test finding team when multiple matches exist (should return first)"""
        team1 = Team.objects.create(
            apisports_id=1,
            name='Team Name',
            description='First team',
            status=TeamStatus.ACTIVE
        )
        
        team2 = Team.objects.create(
            apisports_id=2,
            name='Team Name',  # Same name
            description='Second team',
            status=TeamStatus.ACTIVE
        )
        
        found_team = self.teams_puller._find_team({'id': 999, 'name': 'Team Name'})
        
        # Should return the first match (team1 or team2, depending on database order)
        self.assertIn(found_team, [team1, team2])

    def test_initialization(self):
        """Test TeamsPuller initialization"""
        puller = TeamsPuller()
        
        # Verify client is initialized
        self.assertIsNotNone(puller.client)
        
        # Verify result structure is correct
        expected_result_keys = {
            'success', 'teams_fetched', 'teams_created', 
            'teams_updated', 'errors'
        }
        self.assertEqual(set(puller.result.keys()), expected_result_keys)
        
        # Verify initial values
        self.assertFalse(puller.result['success'])
        self.assertEqual(puller.result['teams_fetched'], 0)
        self.assertEqual(puller.result['teams_created'], 0)
        self.assertEqual(puller.result['teams_updated'], 0)
        self.assertEqual(puller.result['errors'], [])


if __name__ == '__main__':
    unittest.main() 