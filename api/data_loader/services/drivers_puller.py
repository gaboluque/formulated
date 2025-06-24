import logging
from typing import Dict, List, Any, Tuple
from django.db import transaction

from teams.models import Member, MemberRole, Team
from data_loader.lib.openf1_client import OpenF1Client

logger = logging.getLogger(__name__)

class DriversPuller:
    """Service for pulling and syncing driver data from OpenF1"""
    
    def __init__(self):
        """Initialize the service with OpenF1 client"""
        self.client = OpenF1Client()
        
    def pull_and_sync_drivers(self, session_key: str = "latest") -> Dict[str, Any]:
        """
        Pull drivers from OpenF1 and sync with database
        
        Args:
            session_key: Session to pull drivers from (defaults to latest)
            
        Returns:
            Dictionary with sync results
        """
        logger.info(f"Starting driver sync from OpenF1 session: {session_key}")
        
        result = {
            'success': False,
            'drivers_fetched': 0,
            'drivers_created': 0,
            'drivers_updated': 0,
            'errors': [],
            'session_key': session_key
        }
        
        try:
            # Fetch drivers from OpenF1
            openf1_drivers = self._fetch_drivers_from_openf1(session_key)
            result['drivers_fetched'] = len(openf1_drivers)
            
            if not openf1_drivers:
                result['errors'].append("No drivers found in OpenF1 API")
                return result
            
            # Sync drivers with database
            created_count, updated_count, sync_errors = self._sync_drivers_to_database(openf1_drivers)
            
            result['drivers_created'] = created_count
            result['drivers_updated'] = updated_count
            result['errors'].extend(sync_errors)
            result['success'] = True
            
            logger.info(
                f"Driver sync completed: {created_count} created, "
                f"{updated_count} updated, {len(sync_errors)} errors"
            )
            
        except Exception as e:
            error_msg = f"Failed to sync drivers: {str(e)}"
            logger.error(error_msg)
            result['errors'].append(error_msg)
        
        return result
    
    def _fetch_drivers_from_openf1(self, session_key: str) -> List[Dict[str, Any]]:
        """
        Fetch driver data from OpenF1 API
        
        Args:
            session_key: Session to fetch from
            
        Returns:
            List of driver data dictionaries
        """
        try:
            if session_key == "latest":
                drivers = self.client.get_latest_drivers()
            else:
                drivers = self.client.get_drivers(session_key=session_key)
            
            logger.info(f"Fetched {len(drivers)} drivers from OpenF1")
            return drivers
            
        except Exception as e:
            logger.error(f"Error fetching drivers from OpenF1: {str(e)}")
            raise
    
    def _sync_drivers_to_database(self, openf1_drivers: List[Dict[str, Any]]) -> Tuple[int, int, List[str]]:
        """
        Sync OpenF1 driver data with database
        
        Args:
            openf1_drivers: List of driver data from OpenF1
            
        Returns:
            Tuple of (created_count, updated_count, errors)
        """
        created_count = 0
        updated_count = 0
        errors = []
        
        with transaction.atomic():
            for driver_data in openf1_drivers:
                try:
                    created, updated = self._process_single_driver(driver_data)
                    if created:
                        created_count += 1
                    elif updated:
                        updated_count += 1
                        
                except Exception as e:
                    error_msg = f"Error processing driver {driver_data.get('full_name', 'Unknown')}: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)
        
        return created_count, updated_count, errors
    
    def _process_single_driver(self, driver_data: Dict[str, Any]) -> Tuple[bool, bool]:
        """
        Process a single driver - create or update in database
        
        Args:
            driver_data: OpenF1 driver data
            
        Returns:
            Tuple of (was_created, was_updated)
        """
        driver_number = driver_data.get('driver_number')
        if not driver_number:
            raise ValueError("Driver number is required")
        
        # Try to find existing driver by driver_number
        try:
            member = Member.objects.get(driver_number=driver_number)
            # Update existing driver
            updated = self._update_member_from_openf1(member, driver_data)
            return False, updated
            
        except Member.DoesNotExist:
            # Create new driver
            member = self._create_member_from_openf1(driver_data)
            logger.info(f"Created new driver: {member.name} (#{driver_number})")
            return True, False
    
    def _create_member_from_openf1(self, driver_data: Dict[str, Any]) -> Member:
        """
        Create a new Member from OpenF1 driver data
        
        Args:
            driver_data: OpenF1 driver data
            
        Returns:
            Created Member instance
        """
        # Find or create team
        team = self._get_or_create_team(driver_data.get('team_name', 'Unknown Team'))
        
        # Create member
        member = Member.objects.create(
            name=driver_data.get('full_name', ''),
            role=MemberRole.DRIVER,
            description=f"F1 Driver - {driver_data.get('team_name', '')}",
            team=team,
            driver_number=driver_data.get('driver_number'),
            name_acronym=driver_data.get('name_acronym', ''),
            country_code=driver_data.get('country_code', ''),
            headshot_url=driver_data.get('headshot_url', '')
        )
        
        return member
    
    def _update_member_from_openf1(self, member: Member, driver_data: Dict[str, Any]) -> bool:
        """
        Update existing Member with OpenF1 data
        
        Args:
            member: Existing Member instance
            driver_data: OpenF1 driver data
            
        Returns:
            True if member was updated, False if no changes needed
        """
        updated = False
        
        # Update basic fields
        new_name = driver_data.get('full_name', '')
        if member.name != new_name and new_name:
            member.name = new_name
            updated = True
        
        new_acronym = driver_data.get('name_acronym', '')
        if member.name_acronym != new_acronym:
            member.name_acronym = new_acronym
            updated = True
        
        new_country = driver_data.get('country_code', '')
        if member.country_code != new_country:
            member.country_code = new_country
            updated = True
        
        new_headshot = driver_data.get('headshot_url', '')
        if member.headshot_url != new_headshot:
            member.headshot_url = new_headshot
            updated = True
        
        # Update team if different
        new_team_name = driver_data.get('team_name')
        if new_team_name and member.team.name != new_team_name:
            new_team = self._get_or_create_team(new_team_name)
            member.team = new_team
            updated = True
        
        if updated:
            member.save()
            logger.info(f"Updated driver: {member.name} (#{member.driver_number})")
        
        return updated
    
    def _get_or_create_team(self, team_name: str) -> Team:
        """
        Get or create a team by name
        
        Args:
            team_name: Team name from OpenF1
            
        Returns:
            Team instance
        """
        if not team_name or team_name == 'Unknown Team':
            team_name = 'Unknown Team'
        
        team, created = Team.objects.get_or_create(
            name=team_name,
            defaults={
                'description': f'F1 Team - {team_name}',
                'status': 'active'
            }
        )
        
        if created:
            logger.info(f"Created new team: {team_name}")
        
        return team
    
    def get_sync_stats(self) -> Dict[str, Any]:
        """
        Get current driver sync statistics
        
        Returns:
            Dictionary with sync stats
        """
        total_members = Member.objects.count()
        f1_drivers = Member.objects.filter(
            role=MemberRole.DRIVER,
            driver_number__isnull=False
        ).count()
        
        return {
            'total_members': total_members,
            'f1_drivers': f1_drivers,
            'non_driver_members': total_members - f1_drivers
        } 