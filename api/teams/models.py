from django.db import models
import uuid


# Teams

class TeamStatus(models.TextChoices):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=255, choices=TeamStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    logo_url = models.URLField(null=True, blank=True)
    base = models.CharField(max_length=255, null=True, blank=True)
    first_team_entry = models.PositiveIntegerField(null=True, blank=True) # year
    world_championships = models.PositiveIntegerField(null=True, blank=True)
    highest_race_finish = models.PositiveIntegerField(null=True, blank=True)
    pole_positions = models.PositiveIntegerField(null=True, blank=True)
    fastest_laps = models.PositiveIntegerField(null=True, blank=True)
    president = models.CharField(max_length=255, null=True, blank=True)
    director = models.CharField(max_length=255, null=True, blank=True)
    technical_manager = models.CharField(max_length=255, null=True, blank=True)
    chassis = models.CharField(max_length=255, null=True, blank=True)
    engine = models.CharField(max_length=255, null=True, blank=True)
    tyres = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


# Members
    
class MemberRole(models.TextChoices):
    DRIVER = 'driver'
    ENGINEER = 'engineer'
    MANAGER = 'manager'
    OTHER = 'other'

class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=255, choices=MemberRole.choices)
    description = models.TextField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    
    # Driver specific fields
    driver_number = models.PositiveIntegerField(unique=True, null=True, blank=True)
    name_acronym = models.CharField(max_length=3, blank=True)  # VER, HAM, LEC, etc.
    country_code = models.CharField(max_length=3, null=True, blank=True)  # NED, GBR, ESP, etc.
    headshot_url = models.URLField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def is_f1_driver(self):
        """Check if this member is an official F1 driver"""
        return self.role == MemberRole.DRIVER
