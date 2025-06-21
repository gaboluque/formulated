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
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, choices=MemberRole.choices)
    description = models.TextField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
