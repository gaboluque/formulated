from django.contrib.contenttypes.models import ContentType
from interactions.models import Like
from interactions.serializers import LikeSerializer


class LikeService:
    
    @staticmethod
    def check_like(user, obj):
        """Check if user has liked the object"""
        if not user.is_authenticated:
            return {'success': False, 'error': 'Authentication required'}
        
        content_type = ContentType.objects.get_for_model(obj)
        liked = Like.objects.filter(
            user=user,
            record_type=content_type,
            record_id=obj.id
        ).exists()
        
        return {'success': True, 'liked': liked}
    
    @staticmethod
    def create_like(user, obj):
        """Create a like for the given object"""
        if not user.is_authenticated:
            return {'success': False, 'error': 'Authentication required'}
        
        content_type = ContentType.objects.get_for_model(obj)
        
        # Check if already liked
        if Like.objects.filter(
            user=user,
            record_type=content_type,
            record_id=obj.id
        ).exists():
            return {
                'success': False, 
                'error': f'You have already liked this {obj._meta.model_name}'
            }
        
        try:
            # Create the like
            like = Like.objects.create(
                user=user,
                record_type=content_type,
                record_id=obj.id
            )
            
            serializer = LikeSerializer(like)
            return {
                'success': True, 
                'like': serializer.data,
                'message': f'{obj._meta.model_name.title()} liked successfully'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def remove_like(user, obj):
        """Remove a like for the given object"""
        if not user.is_authenticated:
            return {'success': False, 'error': 'Authentication required'}
        
        content_type = ContentType.objects.get_for_model(obj)
        
        try:
            like = Like.objects.get(
                user=user,
                record_type=content_type,
                record_id=obj.id
            )
            like.delete()
            return {
                'success': True,
                'message': f'{obj._meta.model_name.title()} unliked successfully'
            }
        except Like.DoesNotExist:
            return {'success': False, 'error': 'Like not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_likes_for_object(obj):
        """Get all likes for a given object"""
        content_type = ContentType.objects.get_for_model(obj)
        likes = Like.objects.filter(
            record_type=content_type,
            record_id=obj.id
        ).order_by('-created_at')
        
        serializer = LikeSerializer(likes, many=True)
        return {
            'success': True,
            'likes': serializer.data,
            'count': likes.count()
        } 