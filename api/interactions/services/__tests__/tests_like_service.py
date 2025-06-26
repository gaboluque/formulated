import unittest
from unittest.mock import Mock, patch
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from interactions.models import Like
from interactions.services.likes.like_service import LikeService
from teams.models import Team, TeamStatus


class LikeServiceTest(TestCase):
    """Test cases for LikeService"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.anonymous_user = Mock()
        self.anonymous_user.is_authenticated = False
        
        self.test_team = Team.objects.create(
            name='Test Team',
            description='A test team',
            status=TeamStatus.ACTIVE
        )
        
    def test_check_like_unauthenticated_user(self):
        """Test check_like with unauthenticated user"""
        result = LikeService.check_like(self.anonymous_user, self.test_team)
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'Authentication required')
        
    def test_check_like_user_has_not_liked(self):
        """Test check_like when user has not liked the object"""
        result = LikeService.check_like(self.user, self.test_team)
        
        self.assertTrue(result['success'])
        self.assertFalse(result['liked'])
        
    def test_check_like_user_has_liked(self):
        """Test check_like when user has already liked the object"""
        # Create a like first
        content_type = ContentType.objects.get_for_model(self.test_team)
        Like.objects.create(
            user=self.user,
            record_type=content_type,
            record_id=self.test_team.id
        )
        
        result = LikeService.check_like(self.user, self.test_team)
        
        self.assertTrue(result['success'])
        self.assertTrue(result['liked'])
        
    def test_create_like_unauthenticated_user(self):
        """Test create_like with unauthenticated user"""
        result = LikeService.create_like(self.anonymous_user, self.test_team)
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'Authentication required')
        
    def test_create_like_success(self):
        """Test successful like creation"""
        result = LikeService.create_like(self.user, self.test_team)
        
        self.assertTrue(result['success'])
        self.assertIn('like', result)
        self.assertEqual(result['message'], 'Team liked successfully')
        
        # Verify like was created in database
        self.assertTrue(
            Like.objects.filter(
                user=self.user,
                record_type=ContentType.objects.get_for_model(self.test_team),
                record_id=self.test_team.id
            ).exists()
        )
        
    def test_create_like_already_liked(self):
        """Test create_like when user has already liked the object"""
        # Create a like first
        content_type = ContentType.objects.get_for_model(self.test_team)
        Like.objects.create(
            user=self.user,
            record_type=content_type,
            record_id=self.test_team.id
        )
        
        result = LikeService.create_like(self.user, self.test_team)
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'You have already liked this team')
        
    @patch('interactions.services.likes.like_service.Like.objects.create')
    def test_create_like_database_error(self, mock_create):
        """Test create_like when database error occurs"""
        mock_create.side_effect = Exception('Database error')
        
        result = LikeService.create_like(self.user, self.test_team)
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'Database error')
        
    def test_remove_like_unauthenticated_user(self):
        """Test remove_like with unauthenticated user"""
        result = LikeService.remove_like(self.anonymous_user, self.test_team)
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'Authentication required')
        
    def test_remove_like_success(self):
        """Test successful like removal"""
        # Create a like first
        content_type = ContentType.objects.get_for_model(self.test_team)
        like = Like.objects.create(
            user=self.user,
            record_type=content_type,
            record_id=self.test_team.id
        )
        
        result = LikeService.remove_like(self.user, self.test_team)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'Team unliked successfully')
        
        # Verify like was removed from database
        self.assertFalse(
            Like.objects.filter(
                user=self.user,
                record_type=content_type,
                record_id=self.test_team.id
            ).exists()
        )
        
    def test_remove_like_not_found(self):
        """Test remove_like when like doesn't exist"""
        result = LikeService.remove_like(self.user, self.test_team)
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'Like not found')
        
    @patch('interactions.services.likes.like_service.Like.objects.get')
    def test_remove_like_database_error(self, mock_get):
        """Test remove_like when database error occurs"""
        mock_get.side_effect = Exception('Database error')
        
        result = LikeService.remove_like(self.user, self.test_team)
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'Database error')
        
    def test_get_likes_for_object_no_likes(self):
        """Test get_likes_for_object when object has no likes"""
        result = LikeService.get_likes_for_object(self.test_team)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['count'], 0)
        self.assertEqual(len(result['likes']), 0)
        
    def test_get_likes_for_object_with_likes(self):
        """Test get_likes_for_object when object has likes"""
        # Create multiple users and likes
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        content_type = ContentType.objects.get_for_model(self.test_team)
        
        Like.objects.create(
            user=self.user,
            record_type=content_type,
            record_id=self.test_team.id
        )
        
        Like.objects.create(
            user=user2,
            record_type=content_type,
            record_id=self.test_team.id
        )
        
        result = LikeService.get_likes_for_object(self.test_team)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['count'], 2)
        self.assertEqual(len(result['likes']), 2)
        
        # Verify ordering (newest first)
        likes = result['likes']
        self.assertTrue(likes[0]['created_at'] >= likes[1]['created_at'])


if __name__ == '__main__':
    unittest.main() 