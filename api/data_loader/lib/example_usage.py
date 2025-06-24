"""
Example usage of the OpenF1 client

This script demonstrates how to use the OpenF1Client to fetch driver data.
Run this to test the client functionality.
"""

from openf1_client import OpenF1Client
import json


def main():
    """Example usage of the OpenF1 client"""
    
    # Initialize the client
    client = OpenF1Client()
    
    # Test API health
    print("Testing OpenF1 API connection...")
    if not client.health_check():
        print("❌ OpenF1 API is not accessible")
        return
    print("✅ OpenF1 API is accessible")
    
    print("\n" + "="*50)
    
    # Fetch latest drivers
    print("Fetching latest drivers...")
    try:
        drivers = client.get_latest_drivers()
        print(f"✅ Found {len(drivers)} drivers")
        
        # Show first few drivers
        for driver in drivers[:3]:
            print(f"\n🏎️  Driver: {driver.get('full_name', 'N/A')}")
            print(f"   Number: {driver.get('driver_number', 'N/A')}")
            print(f"   Acronym: {driver.get('name_acronym', 'N/A')}")
            print(f"   Country: {driver.get('country_code', 'N/A')}")
            print(f"   Team: {driver.get('team_name', 'N/A')}")
            
    except Exception as e:
        print(f"❌ Error fetching drivers: {e}")
        
    print("\n" + "="*50)
    
    # Fetch specific driver (Max Verstappen - #1)
    print("Fetching specific driver (Max Verstappen - #1)...")
    try:
        driver = client.get_driver_by_number(1)
        if driver:
            print("✅ Found driver:")
            print(json.dumps(driver, indent=2, default=str))
        else:
            print("❌ Driver #1 not found")
            
    except Exception as e:
        print(f"❌ Error fetching driver: {e}")
        
    print("\n" + "="*50)
    
    # Fetch latest meeting info
    print("Fetching latest meeting...")
    try:
        meeting = client.get_latest_meeting()
        if meeting:
            print(f"✅ Latest meeting: {meeting.get('meeting_name', 'N/A')}")
            print(f"   Location: {meeting.get('location', 'N/A')}")
            print(f"   Year: {meeting.get('year', 'N/A')}")
        else:
            print("❌ No meeting found")
            
    except Exception as e:
        print(f"❌ Error fetching meeting: {e}")


if __name__ == "__main__":
    main() 