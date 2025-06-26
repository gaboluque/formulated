from django.db import models
from django.utils import timezone
import uuid


# Circuit

class Circuit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.location}"


# Race

class RaceStatus(models.TextChoices):
    SCHEDULED = 'scheduled'
    ONGOING = 'ongoing'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

class Race(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    apisports_id = models.PositiveIntegerField(unique=True, null=True, blank=True, help_text="APISports F1 API ID")
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, related_name='races')
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_at = models.DateTimeField()
    status = models.CharField(max_length=255, choices=RaceStatus.choices, default=RaceStatus.SCHEDULED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_finished(self):
        """Check if the race is finished - used for review validation"""
        return self.status == RaceStatus.COMPLETED or self.start_at < timezone.now()

    def __str__(self):
        return f"{self.name} at {self.circuit.name}"


# Position

class Position(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='positions')
    driver = models.ForeignKey('teams.Member', on_delete=models.CASCADE, related_name='positions')
    position = models.PositiveIntegerField(null=True, blank=True)
    points = models.PositiveIntegerField(null=True, blank=True)
    laps = models.PositiveIntegerField(null=True, blank=True)
    time = models.CharField(max_length=255, null=True, blank=True)
    pit_stop_count = models.PositiveIntegerField(null=True, blank=True)
    grid = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['race', 'position']  # Ensure unique position per race
        ordering = ['race', 'position']

    def __str__(self):
        return f"{self.driver.name} - Position {self.position} in {self.race.name}"
