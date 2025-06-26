from typing import Dict, Any
from data_loader.lib.apisports_client import APISportsClient
import logging
from teams.models import Team, TeamStatus
from django.db.models import Q
import time

logger = logging.getLogger(__name__)

class TeamsPuller:
    """Service for pulling and syncing team data from APISports F1 API"""
    
    def __init__(self):
        """Initialize the service with APISports F1 API client"""
        self.client = APISportsClient()
        self.result = {
            'success': False,
            'teams_fetched': 0,
            'teams_created': 0,
            'teams_updated': 0,
            'errors': [],
        }
        
    def pull_and_sync_teams(self) -> Dict[str, Any]:
        """
        Pull and sync teams from APISports F1 API
        """
        
        time.sleep(10) # 10 seconds between requests
        
        try:
            teams = self.client.get_teams()
            self.result['teams_fetched'] = len(teams)

            for team in teams:
                logger.info(f"Processing team: {team['name']} (ID: {team.get('id', 'Unknown')})")
                self._process_team(team)
                
        except Exception as e:
            logger.error(f"Error processing teams: {e}")
            self.result['errors'].append(str(e))
            return self.result
        
        self.result['success'] = True
        return self.result
    
    def _process_team(self, team: Dict[str, Any]) -> None:
        """Process a team from APISports F1 API"""
        logger.info(f"Processing team: {team['name']} (ID: {team.get('id', 'Unknown')})")
        
        existing_team = self._find_team(team)
        
        if existing_team:
            logger.info(f"Team {team['name']} already exists (ID: {team.get('id', 'Unknown')}), updating...")
            self._update_team(team, existing_team)
            self.result['teams_updated'] += 1
        else:
            logger.info(f"Team {team['name']} does not exist (ID: {team.get('id', 'Unknown')}), creating...")
            self._create_team(team)
            self.result['teams_created'] += 1
            
        logger.info(f"Team {team['name']} processed successfully")
        
    def _create_team(self, team: Dict[str, Any]) -> None:
        """Create a team from APISports F1 API"""
        Team.objects.create(**self._team_params(team))
        self.result['teams_created'] += 1
        
    def _update_team(self, team: Dict[str, Any], existing_team: Team) -> None:
        """Update a team from APISports F1 API"""
        team_params = self._team_params(team)
        for key, value in team_params.items():
            setattr(existing_team, key, value)
        existing_team.save()
        
    def _team_params(self, team: Dict[str, Any]) -> Dict[str, Any]:
        """Get team parameters from APISports F1 API"""
        return {
            'apisports_id': team['id'],
            'name': team['name'],
            'description': f"Formula 1 Team - {team['name']}",
            'logo_url': team['logo'],
            'base': team['base'],
            'first_team_entry': team['first_team_entry'],
            'world_championships': team['world_championships'],
            'highest_race_finish': team['highest_race_finish']['position'],
            'pole_positions': team['pole_positions'],
            'fastest_laps': team['fastest_laps'],
            'president': team['president'],
            'director': team['director'],
            'technical_manager': team['technical_manager'],
            'chassis': team['chassis'],
            'engine': team['engine'],
            'tyres': team['tyres'],
            'status': TeamStatus.ACTIVE,
        }
        
    def _find_team(self, team: Dict[str, Any]) -> Team:
        """Find a team from APISports F1 API"""
        team_id = team.get('id')
        team_name = team.get('name')
        return Team.objects.filter(Q(apisports_id=team_id) | Q(name=team_name)).first()