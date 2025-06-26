import logging
from datetime import datetime
from typing import Dict, Any
import time
from django.db.models import Q

from teams.models import Member, MemberRole, Team
from data_loader.lib.apisports_client import APISportsClient

logger = logging.getLogger(__name__)

class DriversPuller:
    """Service for pulling and syncing driver data from ApiSports F1"""
    
    def __init__(self):
        """Initialize the service with ApiSports F1 client"""
        self.client = APISportsClient()
        self.result = {
            'success': False,
            'drivers_fetched': 0,
            'drivers_created': 0,
            'drivers_updated': 0,
            'errors': [],
        }
        
    def pull_and_sync_drivers(self) -> Dict[str, Any]:
        """
        Pull drivers from OpenF1 and sync with database
        """
        
        time.sleep(10) # 10 seconds between requests
        
        try:
            current_year = datetime.now().year

            # First get the rankings for the current year since the API
            # doesn't return all drivers in the /drivers endpoint
            rankings = self.client.get_drivers_rankings(current_year)
            self.result['drivers_fetched'] = len(rankings)
            
            # Get the driver IDs from the rankings
            driver_ids = [ranking["driver"]["id"] for ranking in rankings] 
            
            # If no drivers found, return an error
            if not driver_ids:
                self.result['errors'].append("No drivers found in APISports F1 API")
                return self.result
            
            # Process each driver
            for driver_id in driver_ids:                
                # Prevent rate limiting
                time.sleep(10) # 10 seconds between requests

                logger.info(f"Processing driver ID: {driver_id}")
                
                try:
                    driver = self.client.get_driver(driver_id)[0]
                    
                    if not driver:
                        logger.error(f"Driver not found: {driver_id}")
                        self.result['errors'].append(f"Driver not found: {driver_id}")
                        continue

                    self._process_driver(driver)
                except Exception as e:
                    logger.error(f"Error processing driver: {e}")
                    self.result['errors'].append(f"Error processing driver ({driver_id}): {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error processing drivers: {e}")
            self.result['errors'].append(str(e))
            return self.result
        
        self.result['success'] = True
        return self.result
    
    def _process_driver(self, driver: Dict[str, Any]) -> None:
        """Process a driver from APISports F1 API"""
        logger.info(f"Processing driver: {driver['name']} (#{driver['number']}) (ID: {driver['id']})")
        
        # Get driver by api id OR name
        existing_driver = self._find_driver(driver)
        
        if existing_driver:
            logger.info(f"Driver {driver['name']} already exists (ID: {driver['id']}), updating...")
            self._update_driver(driver, existing_driver)
            self.result['drivers_updated'] += 1
        else:
            logger.info(f"Driver {driver['name']} does not exist (ID: {driver['id']}), creating...")
            self._create_driver(driver)
            self.result['drivers_created'] += 1
            
        logger.info(f"Driver {driver['name']} processed successfully")
        
    def _create_driver(self, driver: Dict[str, Any]) -> None:
        """Create a driver from APISports F1 API"""
        Member.objects.create(**self._driver_params(driver))
        self.result['drivers_created'] += 1

    def _update_driver(self, driver: Dict[str, Any], existing_driver: Member) -> None:
        """Update a driver from APISports F1 API"""
        driver_params = self._driver_params(driver)
        for key, value in driver_params.items():
            setattr(existing_driver, key, value)
        existing_driver.save()

    def _driver_params(self, driver: Dict[str, Any]) -> Dict[str, Any]:
        """Get driver parameters from APISports F1 API"""
        # Find team by apisports_id first, then fall back to name
        team = None
        if driver.get('teams') and len(driver['teams']) > 0:
            team_data = driver['teams'][0]['team'] # first team is the current team
            team = self._find_team(team_data)
                
            if not team:
                raise Exception(f"Could not find team for driver {driver['name']}")
        
        return {
            'apisports_id': driver['id'],
            'name': driver['name'],
            'description': f"F1 Driver - {driver['name']}",
            'role': MemberRole.DRIVER,
            'team': team,
            'driver_number': driver['number'],
            'name_acronym': driver['abbr'],
            'country_code': driver['country']['code'],
            'headshot_url': driver['image'],
        }
        
    def _find_driver(self, driver_data: Dict[str, Any]) -> Member:
        """Find a driver from APISports F1 API"""
        driver_id = driver_data.get('id')
        driver_name = driver_data.get('name')
        driver_number = driver_data.get('number')
        return Member.objects.filter(Q(apisports_id=driver_id) | Q(name=driver_name) | Q(driver_number=driver_number)).first()
        
    def _find_team(self, team_data: Dict[str, Any]) -> Team:
        """Find a team from APISports F1 API"""
        team_id = team_data.get('id')
        team_name = team_data.get('name')
        return Team.objects.filter(Q(apisports_id=team_id) | Q(name=team_name)).first()