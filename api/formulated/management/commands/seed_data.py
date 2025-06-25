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
