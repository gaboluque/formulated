import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Review(models.Model):
    """
    User reviews for various record types (teams, races, etc.)
    Uses polymorphic relationships to allow reviews on multiple model types
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    description = models.TextField()
    
    # Polymorphic relationship fields
    record_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    record_id = models.UUIDField()
    record = GenericForeignKey('record_type', 'record_id')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensure a user can only review the same object once
        unique_together = ['user', 'record_type', 'record_id']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.rating}★ on {self.record}"


class Like(models.Model):
    """
    User likes for various record types (teams, races, etc.)
    Uses polymorphic relationships to allow likes on multiple model types
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    
    # Polymorphic relationship fields
    record_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    record_id = models.UUIDField()
    record = GenericForeignKey('record_type', 'record_id')
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure a user can only like the same object once
        unique_together = ['user', 'record_type', 'record_id']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes {self.record}"
