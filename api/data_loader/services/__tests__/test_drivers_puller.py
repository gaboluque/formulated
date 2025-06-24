"""
Test script for DriversPuller service

This script demonstrates how to use the DriversPuller service to sync OpenF1 data.
Run this to test the service functionality.
"""

import os
import sys
import django

# Setup Django environment
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formulated.settings')
django.setup()

from data_loader.services.drivers_puller import DriversPuller
from teams.models import Member, Team
import json


def main():
    """Test the DriversPuller service"""
    
    print("🚀 Testing DriversPuller Service")
    print("=" * 50)
    
    # Initialize service
    puller = DriversPuller()
    
    # Get initial stats
    print("📊 Initial Database Stats:")
    initial_stats = puller.get_sync_stats()
    for key, value in initial_stats.items():
        print(f"   {key}: {value}")
    
    print("\n" + "=" * 50)
    
    # Pull and sync drivers
    print("🔄 Pulling drivers from OpenF1...")
    result = puller.pull_and_sync_drivers()
    
    print(f"\n✅ Sync Results:")
    print(f"   Success: {result['success']}")
    print(f"   Drivers Fetched: {result['drivers_fetched']}")
    print(f"   Drivers Created: {result['drivers_created']}")
    print(f"   Drivers Updated: {result['drivers_updated']}")
    print(f"   Session Key: {result['session_key']}")
    
    if result['errors']:
        print(f"   Errors: {len(result['errors'])}")
        for error in result['errors'][:3]:  # Show first 3 errors
            print(f"     - {error}")
    
    print("\n" + "=" * 50)
    
    # Get final stats
    print("📊 Final Database Stats:")
    final_stats = puller.get_sync_stats()
    for key, value in final_stats.items():
        print(f"   {key}: {value}")
    
    print("\n" + "=" * 50)
    
    # Show some F1 drivers
    print("🏎️  Current F1 Drivers in Database:")
    f1_drivers = Member.objects.filter(
        role='driver',
        driver_number__isnull=False
    ).order_by('driver_number')[:5]
    
    for driver in f1_drivers:
        print(f"   #{driver.driver_number} {driver.name} ({driver.name_acronym}) - {driver.team.name}")
    
    if f1_drivers.count() > 5:
        print(f"   ... and {f1_drivers.count() - 5} more drivers")
    
    print("\n" + "=" * 50)
    
    # Show teams created
    print("🏁 F1 Teams in Database:")
    teams = Team.objects.filter(members__role='driver', members__driver_number__isnull=False
                               ).distinct().order_by('name')
    
    for team in teams:
        driver_count = team.members.filter(role='driver', driver_number__isnull=False).count()
        print(f"   {team.name} ({driver_count} drivers)")
    
    print(f"\n🎉 DriversPuller test completed!")


if __name__ == "__main__":
    main() 