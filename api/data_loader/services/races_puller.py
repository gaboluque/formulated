import logging
from datetime import datetime
from typing import Dict, List, Any
from django.db import transaction
from django.utils.dateparse import parse_datetime
import time

from races.models import Race, Circuit, RaceStatus
from data_loader.lib.apisports_client import APISportsClient

logger = logging.getLogger(__name__)

class RacesPuller:
    """Service for pulling and syncing race data from APISports F1 API"""
    
    def __init__(self):
        """Initialize the service with APISports F1 API client"""
        self.client = APISportsClient()
        self.result = {
            'success': False,
            'races_fetched': 0,
            'races_created': 0,
            'races_updated': 0,
            'circuits_created': 0,
            'circuits_updated': 0,
            'errors': [],
        }
        
    def pull_and_sync_races(self, season: int = None) -> Dict[str, Any]:
        """
        Pull races from APISports F1 API and sync with database
        
        Args:
            season: Year to pull races for. Defaults to current year.
        """
        
        if season is None:
            season = datetime.now().year
        
        try:
            # Get races for the specified season
            races = self.client.get_races(season)
            self.result['races_fetched'] = len(races)
            
            if not races:
                self.result['errors'].append(f"No races found for season {season}")
                return self.result
            
            # Process each race
            for race_data in races:
                try:
                    # Small delay to prevent rate limiting
                    time.sleep(10) # 10 seconds between requests
                    
                    logger.info(f"Processing race: {race_data.get('competition', {}).get('name', 'Unknown')}")
                    self._process_race(race_data)
                    
                except Exception as e:
                    logger.error(f"Error processing race: {e}")
                    self.result['errors'].append(f"Error processing race: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error processing races: {e}")
            self.result['errors'].append(str(e))
            return self.result
        
        self.result['success'] = True
        return self.result
    
    def _process_race(self, race_data: Dict[str, Any]) -> None:
        """Process a race from APISports F1 API"""
        
        with transaction.atomic():
            # First, ensure the circuit exists
            circuit = self._get_or_create_circuit(race_data)
            
            # Then create or update the race
            race_name = race_data.get('competition', {}).get('name', 'Unknown Race')
            
            # Check if race already exists (by name and season)
            existing_race = Race.objects.filter(
                name=race_name,
                circuit=circuit,
                start_at__year=parse_datetime(race_data['date']).year
            ).first()
            
            race_params = self._race_params(race_data, circuit)
            
            if existing_race:
                logger.info(f"Race {race_name} already exists, updating...")
                for key, value in race_params.items():
                    setattr(existing_race, key, value)
                existing_race.save()
                self.result['races_updated'] += 1
            else:
                logger.info(f"Race {race_name} does not exist, creating...")
                Race.objects.create(**race_params)
                self.result['races_created'] += 1
                
        logger.info(f"Race {race_name} processed successfully")
    
    def _get_or_create_circuit(self, race_data: Dict[str, Any]) -> Circuit:
        """Get or create a circuit from race data"""
        
        circuit_data = race_data.get('circuit', {})
        competition_data = race_data.get('competition', {})
        location_data = competition_data.get('location', {})
        
        circuit_name = circuit_data.get('name', 'Unknown Circuit')
        
        # Create location string from country and city
        country = location_data.get('country', '')
        city = location_data.get('city', '')
        location = f"{city}, {country}".strip(', ') if city or country else 'Unknown Location'
        
        # Check if circuit already exists
        circuit = Circuit.objects.filter(name=circuit_name).first()
        
        if circuit:
            # Update location if it's different
            if circuit.location != location:
                circuit.location = location
                circuit.save()
                self.result['circuits_updated'] += 1
        else:
            # Create new circuit
            circuit = Circuit.objects.create(
                name=circuit_name,
                location=location
            )
            self.result['circuits_created'] += 1
            logger.info(f"Created new circuit: {circuit_name}")
        
        return circuit
    
    def _race_params(self, race_data: Dict[str, Any], circuit: Circuit) -> Dict[str, Any]:
        """Get race parameters from APISports F1 API data"""
        
        competition_data = race_data.get('competition', {})
        
        # Map API status to our RaceStatus
        api_status = race_data.get('status', '').lower()
        status_mapping = {
            'completed': RaceStatus.COMPLETED,
            'finished': RaceStatus.COMPLETED,
            'ongoing': RaceStatus.ONGOING,
            'live': RaceStatus.ONGOING,
            'scheduled': RaceStatus.SCHEDULED,
            'cancelled': RaceStatus.CANCELLED,
            'canceled': RaceStatus.CANCELLED,
        }
        status = status_mapping.get(api_status, RaceStatus.SCHEDULED)
        
        # Create description with race details
        description_parts = []
        
        if race_data.get('season'):
            description_parts.append(f"Season: {race_data['season']}")
        
        if race_data.get('type'):
            description_parts.append(f"Type: {race_data['type']}")
        
        if race_data.get('distance'):
            description_parts.append(f"Distance: {race_data['distance']}")
        
        laps = race_data.get('laps', {})
        if laps.get('total'):
            description_parts.append(f"Total Laps: {laps['total']}")
        
        fastest_lap = race_data.get('fastest_lap', {})
        if fastest_lap.get('time'):
            description_parts.append(f"Fastest Lap: {fastest_lap['time']}")
        
        description = " | ".join(description_parts) if description_parts else "Formula 1 Race"
        
        return {
            'circuit': circuit,
            'name': competition_data.get('name', 'Unknown Race'),
            'description': description,
            'start_at': parse_datetime(race_data['date']),
            'status': status,
        }
    
    def get_sync_stats(self) -> Dict[str, int]:
        """Get current database stats for races and circuits"""
        return {
            'total_races': Race.objects.count(),
            'total_circuits': Circuit.objects.count(),
            'completed_races': Race.objects.filter(status=RaceStatus.COMPLETED).count(),
            'scheduled_races': Race.objects.filter(status=RaceStatus.SCHEDULED).count(),
            'ongoing_races': Race.objects.filter(status=RaceStatus.ONGOING).count(),
        } 