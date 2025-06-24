import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from teams.models import Team, Member, TeamStatus, MemberRole
from races.models import Circuit, Race, Position
from interactions.models import Review, Like
from django.db import transaction
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType


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
            self.create_teams_and_drivers()
            
            self.stdout.write(self.style.SUCCESS('Data seeding completed successfully!'))

    def create_superuser(self):
        admin_username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
        admin_email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@formulated.com')
        admin_password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'qwerty123')
        
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
        if Team.objects.count() > 0:
            self.stdout.write(self.style.WARNING('Teams and drivers already exist'))
            return

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

        if Like.objects.count() > 0:
            self.stdout.write(self.style.WARNING('Likes already exist'))
            return

        """Create sample likes for the Monaco race"""
        race_record_type = ContentType.objects.get_for_model(Race)
        
        for user in users:
            like, created = Like.objects.get_or_create(
                user=user,
                record_type=race_record_type,
                record_id=race.id
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Like for Monaco race created by {user.username}')
                ) 