from typing import Dict, Any
from data_loader.lib.apisports_client import APISportsClient
import logging
from teams.models import Team, TeamStatus

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
        """Pull and sync teams from APISports F1 API"""
        
        try:
            teams = self.client.get_teams()
            self.result['teams_fetched'] = len(teams)
            
            if not teams:
                self.result['errors'].append("No teams found in APISports F1 API")
                return self.result
            
            for team in teams:
                logger.info(f"Processing team: {team['name']}")
                self._process_team(team)
                
        except Exception as e:
            logger.error(f"Error processing teams: {e}")
            self.result['errors'].append(str(e))
            return self.result
        
        self.result['success'] = True
        return self.result
    
    def _process_team(self, team: Dict[str, Any]) -> None:
        """Process a team from APISports F1 API"""
        logger.info(f"Processing team: {team['name']}")
        
        # Check if team already exists
        if Team.objects.filter(name=team['name']).exists():
            logger.info(f"Team {team['name']} already exists, updating...")
            team_instance = Team.objects.get(name=team['name'])
            team_instance.update(self._team_params(team))
            team_instance.save()
            self.result['teams_updated'] += 1
        else:
            logger.info(f"Team {team['name']} does not exist, creating...")
            Team.objects.create(
                **self._team_params(team)
            )
            self.result['teams_created'] += 1
            
        logger.info(f"Team {team['name']} processed successfully")
        
    def _team_params(self, team: Dict[str, Any]) -> Dict[str, Any]:
        """Get team parameters from APISports F1 API"""
        return {
            'name': team['name'],
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