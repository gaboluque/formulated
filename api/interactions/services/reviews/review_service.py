from django.contrib.contenttypes.models import ContentType
from interactions.models import Review
from interactions.serializers import ReviewSerializer, ReviewCreateUpdateSerializer


class ReviewService:
    
    @staticmethod
    def get_reviews_for_object(obj):
        """Get all reviews for a given object"""
        content_type = ContentType.objects.get_for_model(obj)
        reviews = Review.objects.filter(
            record_type=content_type,
            record_id=obj.id
        ).order_by('-created_at')
        
        serializer = ReviewSerializer(reviews, many=True)
        return {
            'success': True,
            'reviews': serializer.data,
            'count': reviews.count()
        }
    
    @staticmethod
    def get_user_review(user, obj):
        """Get user's review for a given object"""
        if not user.is_authenticated:
            return {'success': False, 'error': 'Authentication required'}
        
        content_type = ContentType.objects.get_for_model(obj)
        
        try:
            review = Review.objects.get(
                user=user,
                record_type=content_type,
                record_id=obj.id
            )
            serializer = ReviewSerializer(review)
            return {'success': True, 'review': serializer.data}
        except Review.DoesNotExist:
            return {'success': False, 'error': 'Review not found'}
    
    @staticmethod
    def create_review(user, obj, data):
        """Create a review for the given object"""
        if not user.is_authenticated:
            return {'success': False, 'error': 'Authentication required'}
        
        content_type = ContentType.objects.get_for_model(obj)
        
        # Check if user already has a review
        if Review.objects.filter(
            user=user,
            record_type=content_type,
            record_id=obj.id
        ).exists():
            return {
                'success': False, 
                'error': f'You have already reviewed this {obj._meta.model_name}'
            }
        
        # Validate the data
        serializer = ReviewCreateUpdateSerializer(data=data)
        if not serializer.is_valid():
            return {'success': False, 'error': serializer.errors}
        
        try:
            # Create the review
            review = Review.objects.create(
                user=user,
                record_type=content_type,
                record_id=obj.id,
                **serializer.validated_data
            )
            
            response_serializer = ReviewSerializer(review)
            return {
                'success': True,
                'review': response_serializer.data,
                'message': f'{obj._meta.model_name.title()} reviewed successfully'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def update_review(user, obj, data):
        """Update user's review for the given object"""
        if not user.is_authenticated:
            return {'success': False, 'error': 'Authentication required'}
        
        content_type = ContentType.objects.get_for_model(obj)
        
        try:
            review = Review.objects.get(
                user=user,
                record_type=content_type,
                record_id=obj.id
            )
        except Review.DoesNotExist:
            return {'success': False, 'error': 'Review not found'}
        
        # Validate the data
        serializer = ReviewCreateUpdateSerializer(review, data=data)
        if not serializer.is_valid():
            return {'success': False, 'error': serializer.errors}
        
        try:
            serializer.save()
            response_serializer = ReviewSerializer(review)
            return {
                'success': True,
                'review': response_serializer.data,
                'message': f'{obj._meta.model_name.title()} review updated successfully'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def delete_review(user, obj):
        """Delete user's review for the given object"""
        if not user.is_authenticated:
            return {'success': False, 'error': 'Authentication required'}
        
        content_type = ContentType.objects.get_for_model(obj)
        
        try:
            review = Review.objects.get(
                user=user,
                record_type=content_type,
                record_id=obj.id
            )
            review.delete()
            return {
                'success': True,
                'message': f'{obj._meta.model_name.title()} review deleted successfully'
            }
        except Review.DoesNotExist:
            return {'success': False, 'error': 'Review not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)} 