from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import datetime
from data_loader.services.races_puller import RacesPuller


class Command(BaseCommand):
    help = 'Pull races data from APISports F1 API and sync with database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--season',
            type=int,
            default=None,
            help='Season year to pull races for (default: current year)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes'
        )

    def handle(self, *args, **options):
        season = options['season'] or datetime.now().year
        dry_run = options['dry_run']
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting to pull races data for {season} season...')
        )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No changes will be made to the database')
            )
        
        try:
            if not dry_run:
                with transaction.atomic():
                    result = self._pull_races(season)
            else:
                result = self._pull_races_dry_run(season)
                
            self._display_results(result, season)
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error pulling races data: {str(e)}')
            )
            raise

    def _pull_races(self, season):
        """Pull races data and sync with database"""
        puller = RacesPuller()
        
        # Get initial stats
        initial_stats = puller.get_sync_stats()
        self.stdout.write(f'Initial stats: {initial_stats}')
        
        # Pull and sync
        result = puller.pull_and_sync_races(season)
        
        # Get final stats
        final_stats = puller.get_sync_stats()
        result['initial_stats'] = initial_stats
        result['final_stats'] = final_stats
        
        return result

    def _pull_races_dry_run(self, season):
        """Simulate pulling races data without making changes"""
        puller = RacesPuller()
        
        # Get current stats
        current_stats = puller.get_sync_stats()
        
        # In a real dry run, we would fetch from API but not save
        # For now, just return current stats
        return {
            'success': True,
            'races_fetched': 0,
            'races_created': 0,
            'races_updated': 0,
            'circuits_created': 0,
            'circuits_updated': 0,
            'errors': [],
            'initial_stats': current_stats,
            'final_stats': current_stats,
            'dry_run': True
        }

    def _display_results(self, result, season):
        """Display the results of the pull operation"""
        
        if result['success']:
            self.stdout.write(
                self.style.SUCCESS(f'✅ Successfully pulled races for {season} season!')
            )
        else:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to pull races for {season} season')
            )
        
        # Display sync statistics
        self.stdout.write('\n📊 Sync Results:')
        self.stdout.write(f'   Races Fetched: {result["races_fetched"]}')
        self.stdout.write(f'   Races Created: {result["races_created"]}')
        self.stdout.write(f'   Races Updated: {result["races_updated"]}')
        self.stdout.write(f'   Circuits Created: {result["circuits_created"]}')
        self.stdout.write(f'   Circuits Updated: {result["circuits_updated"]}')
        
        # Display database statistics if available
        if 'initial_stats' in result and 'final_stats' in result:
            self.stdout.write('\n📈 Database Changes:')
            initial = result['initial_stats']
            final = result['final_stats']
            
            for key in final.keys():
                change = final[key] - initial[key]
                if change != 0:
                    self.stdout.write(f'   {key}: {initial[key]} → {final[key]} ({change:+d})')
                else:
                    self.stdout.write(f'   {key}: {final[key]} (no change)')
        
        # Display errors if any
        if result['errors']:
            self.stdout.write('\n❗ Errors encountered:')
            for i, error in enumerate(result['errors'][:5], 1):  # Show first 5 errors
                self.stdout.write(f'   {i}. {error}')
            
            if len(result['errors']) > 5:
                self.stdout.write(f'   ... and {len(result["errors"]) - 5} more errors')
        
        if result.get('dry_run'):
            self.stdout.write(
                self.style.WARNING('\nℹ️  This was a dry run - no changes were made to the database')
            ) 