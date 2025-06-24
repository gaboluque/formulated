"""
OpenF1 API Client

A simple client for fetching data from the OpenF1 API.
Focuses on data retrieval without business logic or data storage.
"""

import requests
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class OpenF1Client:
    """Client for interacting with the OpenF1 API"""
    
    BASE_URL = "https://api.openf1.org/v1"
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the OpenF1 client
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Formulated-F1-App/1.0'
        })
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Make a request to the OpenF1 API
        
        Args:
            endpoint: API endpoint (without base URL)
            params: Query parameters
            
        Returns:
            List of data from the API response
            
        Raises:
            requests.RequestException: If the request fails
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            logger.info(f"Making request to OpenF1: {url}")
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully fetched {len(data)} records from {endpoint}")
            return data
            
        except requests.RequestException as e:
            logger.error(f"Error fetching data from OpenF1 {endpoint}: {str(e)}")
            raise
    
    # Driver Data Methods
    
    def get_drivers(self, 
                   session_key: Optional[str] = None,
                   meeting_key: Optional[str] = None,
                   driver_number: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Fetch driver data from OpenF1
        
        Args:
            session_key: Specific session key (optional)
            meeting_key: Specific meeting key (optional) 
            driver_number: Specific driver number (optional)
            
        Returns:
            List of driver data dictionaries
        """
        params = {}
        if session_key:
            params['session_key'] = session_key
        if meeting_key:
            params['meeting_key'] = meeting_key
        if driver_number:
            params['driver_number'] = driver_number
            
        return self._make_request("drivers", params)
    
    def get_latest_drivers(self) -> List[Dict[str, Any]]:
        """
        Fetch drivers from the latest session
        
        Returns:
            List of driver data from the most recent session
        """
        return self.get_drivers(session_key="latest")
    
    def get_driver_by_number(self, driver_number: int, session_key: str = "latest") -> Optional[Dict[str, Any]]:
        """
        Fetch a specific driver by their number
        
        Args:
            driver_number: F1 driver number
            session_key: Session key (defaults to "latest")
            
        Returns:
            Driver data dictionary or None if not found
        """
        drivers = self.get_drivers(driver_number=driver_number, session_key=session_key)
        return drivers[0] if drivers else None
    
    # Meeting and Session Methods (for context)
    
    def get_meetings(self, 
                    year: Optional[int] = None,
                    country_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Fetch meeting (race weekend) data
        
        Args:
            year: Specific year (optional)
            country_name: Specific country (optional)
            
        Returns:
            List of meeting data dictionaries
        """
        params = {}
        if year:
            params['year'] = year
        if country_name:
            params['country_name'] = country_name
            
        return self._make_request("meetings", params)
    
    def get_sessions(self,
                    meeting_key: Optional[str] = None,
                    session_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Fetch session data
        
        Args:
            meeting_key: Specific meeting key (optional)
            session_name: Specific session name like "Race", "Qualifying" (optional)
            
        Returns:
            List of session data dictionaries
        """
        params = {}
        if meeting_key:
            params['meeting_key'] = meeting_key
        if session_name:
            params['session_name'] = session_name
            
        return self._make_request("sessions", params)
    
    def get_latest_meeting(self) -> Optional[Dict[str, Any]]:
        """
        Get the latest meeting
        
        Returns:
            Latest meeting data or None
        """
        meetings = self._make_request("meetings", {"meeting_key": "latest"})
        return meetings[0] if meetings else None
    
    # Utility Methods
    
    def health_check(self) -> bool:
        """
        Check if the OpenF1 API is accessible
        
        Returns:
            True if API is accessible, False otherwise
        """
        try:
            # Try to fetch latest meeting as a simple health check
            self.get_latest_meeting()
            return True
        except Exception as e:
            logger.error(f"OpenF1 API health check failed: {str(e)}")
            return False 