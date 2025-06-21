from django.db import models
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

class Race(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, related_name='races')
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} at {self.circuit.name}"


# Position

class Position(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='positions')
    driver = models.ForeignKey('teams.Member', on_delete=models.CASCADE, related_name='positions')
    position = models.PositiveIntegerField()
    points = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['race', 'position']  # Ensure unique position per race
        ordering = ['race', 'position']

    def __str__(self):
        return f"{self.driver.name} - Position {self.position} in {self.race.name}"
