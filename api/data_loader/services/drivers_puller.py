import logging
from datetime import datetime
from typing import Dict, List, Any, Tuple
from django.db import transaction
import time

from teams.models import Member, MemberRole, Team
from data_loader.lib.apisports_client import APISportsClient

logger = logging.getLogger(__name__)

class DriversPuller:
    """Service for pulling and syncing driver data from OpenF1"""
    
    def __init__(self):
        """Initialize the service with OpenF1 client"""
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
        
        try:
            current_year = datetime.now().year
            
            # First get the rankings for the current year since the API
            # doesn't return all drivers in the /drivers endpoint
            rankings = self.client.get_drivers_rankings(current_year)
            self.result['drivers_fetched'] = len(rankings)
            
            # Get the driver IDs from the rankings
            driver_ids = [ranking["driver"]["id"] for ranking in rankings] 
            
            print("driver_ids", driver_ids)           
        
            # If no drivers found, return an error
            if not driver_ids:
                self.result['errors'].append("No drivers found in APISports F1 API")
                return self.result
            
            # Process each driver
            for driver_id in driver_ids:                
                # Prevent rate limiting
                time.sleep(10) # 10 seconds between requests

                logger.info(f"Processing driver: {driver_id}")
                
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
        logger.info(f"Processing driver: {driver['name']}")
        
        # Check if driver already exists
        if Member.objects.filter(name=driver['name']).exists():
            logger.info(f"Driver {driver['name']} already exists, updating...")
            driver_instance = Member.objects.get(name=driver['name'])
            driver_instance.update(self._driver_params(driver))
            driver_instance.save()
            self.result['drivers_updated'] += 1
        else:
            logger.info(f"Driver {driver['name']} does not exist, creating...")
            Member.objects.create(
                **self._driver_params(driver)
            )
            self.result['drivers_created'] += 1
            
        logger.info(f"Driver {driver['name']} processed successfully")

    def _driver_params(self, driver: Dict[str, Any]) -> Dict[str, Any]:
        """Get driver parameters from APISports F1 API"""
        return {
            'name': driver['name'],
            'role': MemberRole.DRIVER,
            'team': Team.objects.get(name=driver['teams'][0]['team']['name']),
            'driver_number': driver['number'],
            'name_acronym': driver['abbr'],
            'country_code': driver['country']['code'],
            'headshot_url': driver['image'],
        }