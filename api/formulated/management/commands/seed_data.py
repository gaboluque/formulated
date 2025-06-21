import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from teams.models import Team, Member, TeamStatus, MemberRole
from django.db import transaction


class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write(self.style.SUCCESS('Starting data seeding...'))
            
            # Create superuser
            self.create_superuser()
            
            # Create normal user
            self.create_normal_user()
            
            # Create test team
            team = self.create_test_team()
            
            # Create test member
            self.create_test_member(team)
            
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

    def create_test_team(self):
        team_name = 'Ferrari'
        
        team, created = Team.objects.get_or_create(
            name=team_name,
            defaults={
                'description': 'Scuderia Ferrari, the legendary Formula 1 racing team',
                'status': TeamStatus.ACTIVE
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Team "{team_name}" created successfully')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Team "{team_name}" already exists')
            )
        
        return team

    def create_test_member(self, team):
        member_name = 'Lewis Hamilton'
        
        member, created = Member.objects.get_or_create(
            name=member_name,
            team=team,
            defaults={
                'role': MemberRole.DRIVER,
                'description': 'Seven-time Formula 1 World Champion and legendary driver'
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Member "{member_name}" created successfully')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Member "{member_name}" already exists')
            ) 