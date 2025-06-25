"""
APISports F1 API Client

A simple client for fetching data from the APISports F1 API.
"""

import requests
from typing import Dict, List, Optional, Any
import logging
import os

logger = logging.getLogger(__name__)


class APISportsClient:
    """Client for interacting with the APISports F1 API"""
    
    BASE_URL = "https://api-formula-1.p.rapidapi.com"
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.headers = {
            "X-RapidAPI-Key": os.getenv("APISPORTS_API_KEY"),
            "X-RapidAPI-Host": "api-formula-1.p.rapidapi.com"
        }
        
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a request to the APISports F1 API"""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            logger.info(f"Making request to APISports F1 API: {url}")
            response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
            response.raise_for_status()
            logger.info(f"Successfully fetched {len(response.json())} records from {endpoint}")
            print(response.json())
            return response.json()['response'] or []
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request to {url}: {e}")
            raise
        
    def get_driver(self, driver_id: str) -> Dict[str, Any]:
        """Get a driver from the APISports F1 API"""
        endpoint = f"/drivers?id={driver_id}"
        return self._make_request(endpoint)
    
    def get_teams(self) -> List[Dict[str, Any]]:
        """Get all teams from the APISports F1 API"""
        endpoint = "/teams"
        return self._make_request(endpoint)
    
    def get_drivers_rankings(self, season: int) -> List[Dict[str, Any]]:
        """Get the drivers rankings from the APISports F1 API"""
        endpoint = f"/rankings/drivers?season={season}"
        return self._make_request(endpoint)
    
    def get_races(self, season: int, race_type: str = "race") -> List[Dict[str, Any]]:
        """Get races from the APISports F1 API"""
        endpoint = "/races"
        params = {
            "season": season,
            "type": race_type
        }
        return self._make_request(endpoint, params)
    
    def get_competitions(self, season: int) -> List[Dict[str, Any]]:
        """Get competitions (race weekends) from the APISports F1 API"""
        endpoint = "/competitions"
        params = {"season": season}
        return self._make_request(endpoint, params)