import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from teams.models import Team, Member, TeamStatus, MemberRole
from races.models import Circuit, Race, Position
from django.db import transaction
from django.utils import timezone


class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write(self.style.SUCCESS('Starting data seeding...'))
            
            # Create superuser
            self.create_superuser()
            
            # Create normal user
            self.create_normal_user()
            
            # Create teams and drivers
            teams = self.create_teams_and_drivers()
            
            # Create Monaco circuit
            monaco_circuit = self.create_monaco_circuit()
            
            # Create Monaco 2024 race
            monaco_race = self.create_monaco_2024_race(monaco_circuit)
            
            # Create race positions
            self.create_monaco_2024_positions(monaco_race, teams)
            
            self.stdout.write(self.style.SUCCESS('Data seeding completed successfully!'))

    def create_superuser(self):
        admin_username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
        admin_email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@formulated.com')
        admin_password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin123')
        
        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{admin_username}" created successfully')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Superuser "{admin_username}" already exists')
            )

    def create_normal_user(self):
        username = 'testuser'
        email = 'test@formulated.com'
        password = 'qwerty123'
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name='John',
                last_name='Doe'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Normal user "{username}" created successfully')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Normal user "{username}" already exists')
            )

    def create_teams_and_drivers(self):
        teams_data = [
            {
                'name': 'Ferrari',
                'description': 'Scuderia Ferrari, the legendary Formula 1 racing team',
                'drivers': [
                    {'name': 'Charles Leclerc', 'description': 'Monégasque racing driver for Ferrari'},
                    {'name': 'Carlos Sainz Jr.', 'description': 'Spanish racing driver for Ferrari'}
                ]
            },
            {
                'name': 'McLaren',
                'description': 'McLaren Racing, British Formula 1 team',
                'drivers': [
                    {'name': 'Oscar Piastri', 'description': 'Australian racing driver for McLaren'},
                    {'name': 'Lando Norris', 'description': 'British racing driver for McLaren'}
                ]
            },
            {
                'name': 'Red Bull Racing',
                'description': 'Red Bull Racing Honda RBPT, Austrian Formula 1 team',
                'drivers': [
                    {'name': 'Max Verstappen', 'description': 'Dutch racing driver and multiple-time World Champion'},
                    {'name': 'Sergio Pérez', 'description': 'Mexican racing driver for Red Bull Racing'}
                ]
            },
            {
                'name': 'Mercedes',
                'description': 'Mercedes-AMG Petronas Formula One Team',
                'drivers': [
                    {'name': 'Lewis Hamilton', 'description': 'Seven-time Formula 1 World Champion'},
                    {'name': 'George Russell', 'description': 'British racing driver for Mercedes'}
                ]
            },
            {
                'name': 'Aston Martin',
                'description': 'Aston Martin Aramco Cognizant Formula One Team',
                'drivers': [
                    {'name': 'Fernando Alonso', 'description': 'Spanish racing driver and two-time World Champion'},
                    {'name': 'Lance Stroll', 'description': 'Canadian racing driver for Aston Martin'}
                ]
            }
        ]
        
        teams = {}
        
        for team_data in teams_data:
            team, created = Team.objects.get_or_create(
                name=team_data['name'],
                defaults={
                    'description': team_data['description'],
                    'status': TeamStatus.ACTIVE
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Team "{team_data["name"]}" created successfully')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Team "{team_data["name"]}" already exists')
                )
            
            teams[team_data['name']] = {'team': team, 'drivers': []}
            
            # Create drivers for this team
            for driver_data in team_data['drivers']:
                member, created = Member.objects.get_or_create(
                    name=driver_data['name'],
                    team=team,
                    defaults={
                        'role': MemberRole.DRIVER,
                        'description': driver_data['description']
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Driver "{driver_data["name"]}" created successfully')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Driver "{driver_data["name"]}" already exists')
                    )
                
                teams[team_data['name']]['drivers'].append(member)
        
        return teams

    def create_monaco_circuit(self):
        circuit, created = Circuit.objects.get_or_create(
            name='Circuit de Monaco',
            defaults={
                'location': 'Monte Carlo, Monaco'
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Monaco circuit created successfully')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Monaco circuit already exists')
            )
        
        return circuit

    def create_monaco_2024_race(self, circuit):
        race_date = timezone.make_aware(datetime(2024, 5, 26, 15, 0))  # Monaco GP 2024 date
        
        race, created = Race.objects.get_or_create(
            name='Monaco Grand Prix 2024',
            circuit=circuit,
            defaults={
                'description': 'The 2024 Monaco Grand Prix, round 8 of the 2024 Formula 1 World Championship',
                'start_at': race_date
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Monaco 2024 race created successfully')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Monaco 2024 race already exists')
            )
        
        return race

    def create_monaco_2024_positions(self, race, teams):
        # Monaco 2024 actual race results
        race_results = [
            {'driver': 'Charles Leclerc', 'team': 'Ferrari', 'position': 1, 'points': 25},
            {'driver': 'Oscar Piastri', 'team': 'McLaren', 'position': 2, 'points': 18},
            {'driver': 'Carlos Sainz Jr.', 'team': 'Ferrari', 'position': 3, 'points': 15},
            {'driver': 'Lando Norris', 'team': 'McLaren', 'position': 4, 'points': 12},
            {'driver': 'George Russell', 'team': 'Mercedes', 'position': 5, 'points': 10},
            {'driver': 'Max Verstappen', 'team': 'Red Bull Racing', 'position': 6, 'points': 8},
            {'driver': 'Lewis Hamilton', 'team': 'Mercedes', 'position': 7, 'points': 6},
            {'driver': 'Fernando Alonso', 'team': 'Aston Martin', 'position': 8, 'points': 4},
            {'driver': 'Lance Stroll', 'team': 'Aston Martin', 'position': 9, 'points': 2},
            {'driver': 'Sergio Pérez', 'team': 'Red Bull Racing', 'position': 10, 'points': 1},
        ]
        
        for result in race_results:
            # Find the driver
            driver = None
            if result['team'] in teams:
                for team_driver in teams[result['team']]['drivers']:
                    if team_driver.name == result['driver']:
                        driver = team_driver
                        break
            
            if driver:
                position, created = Position.objects.get_or_create(
                    race=race,
                    driver=driver,
                    defaults={
                        'position': result['position'],
                        'points': result['points']
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Position {result["position"]} for {result["driver"]} created successfully')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Position for {result["driver"]} already exists')
                    ) 