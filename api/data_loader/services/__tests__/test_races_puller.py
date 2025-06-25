"""
Test script for RacesPuller service

This script demonstrates how to use the RacesPuller service to sync APISports F1 API data.
Run this to test the service functionality.
"""

import os
import sys
import django

# Setup Django environment
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formulated.settings')
django.setup()

from data_loader.services.races_puller import RacesPuller
from races.models import Race, Circuit, RaceStatus, Position
from teams.models import Member, MemberRole
from datetime import datetime
import json


def main():
    """Test the RacesPuller service"""
    
    print("🏁 Testing RacesPuller Service")
    print("=" * 50)
    
    # Initialize service
    puller = RacesPuller()
    
    # Get initial stats
    print("📊 Initial Database Stats:")
    initial_stats = puller.get_sync_stats()
    for key, value in initial_stats.items():
        print(f"   {key}: {value}")
    
    print("\n" + "=" * 50)
    
    # Pull and sync races for current season
    current_season = datetime.now().year
    print(f"🔄 Pulling races from APISports F1 API for {current_season} season...")
    result = puller.pull_and_sync_races(current_season)
    
    print(f"\n✅ Sync Results:")
    print(f"   Success: {result['success']}")
    print(f"   Races Fetched: {result['races_fetched']}")
    print(f"   Races Created: {result['races_created']}")
    print(f"   Races Updated: {result['races_updated']}")
    print(f"   Circuits Created: {result['circuits_created']}")
    print(f"   Circuits Updated: {result['circuits_updated']}")
    print(f"   Positions Created: {result['positions_created']}")
    print(f"   Positions Updated: {result['positions_updated']}")
    
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
    
    # Show some recent races
    print("🏎️  Recent Races in Database:")
    recent_races = Race.objects.order_by('-start_at')[:5]
    
    for race in recent_races:
        status_emoji = {
            RaceStatus.COMPLETED: "✅",
            RaceStatus.ONGOING: "🔄",
            RaceStatus.SCHEDULED: "📅",
            RaceStatus.CANCELLED: "❌"
        }.get(race.status, "❓")
        
        print(f"   {status_emoji} {race.name} at {race.circuit.name}")
        print(f"      📍 {race.circuit.location}")
        print(f"      🗓️  {race.start_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"      📝 {race.description[:60]}{'...' if len(race.description) > 60 else ''}")
        print()
    
    if Race.objects.count() > 5:
        print(f"   ... and {Race.objects.count() - 5} more races")
    
    print("\n" + "=" * 50)
    
    # Show circuits created
    print("🏟️  F1 Circuits in Database:")
    circuits = Circuit.objects.order_by('name')
    
    for circuit in circuits:
        race_count = circuit.races.count()
        completed_races = circuit.races.filter(status=RaceStatus.COMPLETED).count()
        print(f"   🏟️  {circuit.name}")
        print(f"      📍 {circuit.location}")
        print(f"      🏁 {race_count} total races ({completed_races} completed)")
        print()
    
    print("\n" + "=" * 50)
    
    # Show races by status
    print("📊 Races by Status:")
    for status, label in RaceStatus.choices:
        count = Race.objects.filter(status=status).count()
        if count > 0:
            status_emoji = {
                RaceStatus.COMPLETED: "✅",
                RaceStatus.ONGOING: "🔄",
                RaceStatus.SCHEDULED: "📅",
                RaceStatus.CANCELLED: "❌"
            }.get(status, "❓")
            print(f"   {status_emoji} {label.title()}: {count}")
    
    print(f"\n🎉 RacesPuller test completed!")
    
    # Show some position data if any exists
    print("\n" + "=" * 50)
    print("🏆 Race Positions Sample:")
    
    recent_positions = Position.objects.select_related('race', 'driver', 'driver__team').order_by('-race__start_at', 'position')[:10]
    
    if recent_positions:
        current_race = None
        for position in recent_positions:
            if current_race != position.race:
                current_race = position.race
                print(f"\n   🏁 {position.race.name}")
                print(f"      📅 {position.race.start_at.strftime('%Y-%m-%d')}")
            
            print(f"      #{position.position:2d} - {position.driver.name} ({position.driver.name_acronym})")
            print(f"           Team: {position.driver.team.name}")
            print(f"           Points: {position.points}, Laps: {position.laps}")
            if position.time:
                print(f"           Time: {position.time}")
    else:
        print("   No position data available yet.")
        print("   Note: Make sure drivers exist in the database before running races sync.")
        
        # Show available drivers
        drivers = Member.objects.filter(role=MemberRole.DRIVER).order_by('name')[:5]
        if drivers:
            print(f"\n   Available F1 Drivers ({drivers.count()} total):")
            for driver in drivers:
                abbr = f"({driver.name_acronym})" if driver.name_acronym else ""
                num = f"#{driver.driver_number}" if driver.driver_number else ""
                print(f"      {driver.name} {abbr} {num} - {driver.team.name}")
        else:
            print("   No F1 drivers found. Run the drivers puller first.")


if __name__ == "__main__":
    main() 