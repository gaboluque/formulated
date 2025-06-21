from rest_framework import serializers
from interactions.models import Like, Review
from django.contrib.contenttypes.models import ContentType

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    record_type = serializers.SlugRelatedField(
        slug_field='model',
        read_only=True
    )
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'record_type', 'record_id', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
        
class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['record_id']
        
    def validate_record_id(self, value):
        if Like.objects.filter(user=self.context['request'].user, record_id=value).exists():
            raise serializers.ValidationError("You have already liked this record")
        return value

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    record_type = serializers.SlugRelatedField(
        slug_field='model',
        read_only=True
    )
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'description', 'record_type', 'record_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

class ReviewCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'description']
    
    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value