import unittest
from unittest.mock import Mock, patch
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from interactions.models import Review
from interactions.services.reviews.review_service import ReviewService
from teams.models import Team, TeamStatus


class ReviewServiceTest(TestCase):
    """Test cases for ReviewService"""

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
        
        self.valid_review_data = {
            'rating': 4,
            'description': 'Great team with excellent performance!'
        }
        
        self.invalid_review_data = {
            'rating': 6,  # Invalid rating (should be 1-5)
            'description': ''  # Empty description
        }
        
    def test_get_reviews_for_object_no_reviews(self):
        """Test get_reviews_for_object when object has no reviews"""
        result = ReviewService.get_reviews_for_object(self.test_team)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['count'], 0)
        self.assertEqual(len(result['reviews']), 0)
        
    def test_get_reviews_for_object_with_reviews(self):
        """Test get_reviews_for_object when object has reviews"""
        # Create multiple users and reviews
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        content_type = ContentType.objects.get_for_model(self.test_team)
        
        Review.objects.create(
            user=self.user,
            record_type=content_type,
            record_id=self.test_team.id,
            rating=5,
            description='Excellent team!'
        )
        
        Review.objects.create(
            user=user2,
            record_type=content_type,
            record_id=self.test_team.id,
            rating=3,
            description='Average performance'
        )
        
        result = ReviewService.get_reviews_for_object(self.test_team)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['count'], 2)
        self.assertEqual(len(result['reviews']), 2)
        
        # Verify ordering (newest first)
        reviews = result['reviews']
        self.assertTrue(reviews[0]['created_at'] >= reviews[1]['created_at'])
        
    def test_get_user_review_unauthenticated_user(self):
        """Test get_user_review with unauthenticated user"""
        result = ReviewService.get_user_review(self.anonymous_user, self.test_team)
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'Authentication required')
        
    def test_get_user_review_not_found(self):
        """Test get_user_review when user has no review for object"""
        result = ReviewService.get_user_review(self.user, self.test_team)
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'Review not found')
        
    def test_get_user_review_success(self):
        """Test get_user_review when user has a review for object"""
        # Create a review first
        content_type = ContentType.objects.get_for_model(self.test_team)
        review = Review.objects.create(
            user=self.user,
            record_type=content_type,
            record_id=self.test_team.id,
            rating=4,
            description='Good team'
        )
        
        result = ReviewService.get_user_review(self.user, self.test_team)
        
        self.assertTrue(result['success'])
        self.assertIn('review', result)
        self.assertEqual(result['review']['rating'], 4)
        self.assertEqual(result['review']['description'], 'Good team')
        
    def test_create_review_unauthenticated_user(self):
        """Test create_review with unauthenticated user"""
        result = ReviewService.create_review(
            self.anonymous_user, 
            self.test_team, 
            self.valid_review_data
        )
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'Authentication required')
        
    def test_create_review_success(self):
        """Test successful review creation"""
        result = ReviewService.create_review(
            self.user, 
            self.test_team, 
            self.valid_review_data
        )
        
        self.assertTrue(result['success'])
        self.assertIn('review', result)
        self.assertEqual(result['message'], 'Team reviewed successfully')
        
        # Verify review was created in database
        self.assertTrue(
            Review.objects.filter(
                user=self.user,
                record_type=ContentType.objects.get_for_model(self.test_team),
                record_id=self.test_team.id
            ).exists()
        )
        
    def test_create_review_already_reviewed(self):
        """Test create_review when user has already reviewed the object"""
        # Create a review first
        content_type = ContentType.objects.get_for_model(self.test_team)
        Review.objects.create(
            user=self.user,
            record_type=content_type,
            record_id=self.test_team.id,
            rating=3,
            description='Previous review'
        )
        
        result = ReviewService.create_review(
            self.user, 
            self.test_team, 
            self.valid_review_data
        )
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'You have already reviewed this team')
        
    @patch('interactions.services.reviews.review_service.ReviewCreateUpdateSerializer')
    def test_create_review_invalid_data(self, mock_serializer_class):
        """Test create_review with invalid data"""
        mock_serializer = Mock()
        mock_serializer.is_valid.return_value = False
        mock_serializer.errors = {'rating': ['Rating must be between 1 and 5']}
        mock_serializer_class.return_value = mock_serializer
        
        result = ReviewService.create_review(
            self.user, 
            self.test_team, 
            self.invalid_review_data
        )
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], {'rating': ['Rating must be between 1 and 5']})
        
    @patch('interactions.services.reviews.review_service.Review.objects.create')
    def test_create_review_database_error(self, mock_create):
        """Test create_review when database error occurs"""
        mock_create.side_effect = Exception('Database error')
        
        result = ReviewService.create_review(
            self.user, 
            self.test_team, 
            self.valid_review_data
        )
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'Database error')
        
    def test_update_review_unauthenticated_user(self):
        """Test update_review with unauthenticated user"""
        result = ReviewService.update_review(
            self.anonymous_user, 
            self.test_team, 
            self.valid_review_data
        )
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'Authentication required')
        
    def test_update_review_not_found(self):
        """Test update_review when user has no existing review"""
        result = ReviewService.update_review(
            self.user, 
            self.test_team, 
            self.valid_review_data
        )
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'Review not found')
        
    def test_update_review_success(self):
        """Test successful review update"""
        # Create a review first
        content_type = ContentType.objects.get_for_model(self.test_team)
        review = Review.objects.create(
            user=self.user,
            record_type=content_type,
            record_id=self.test_team.id,
            rating=3,
            description='Initial review'
        )
        
        updated_data = {
            'rating': 5,
            'description': 'Updated review - much better!'
        }
        
        with patch('interactions.services.reviews.review_service.ReviewCreateUpdateSerializer') as mock_serializer_class:
            mock_serializer = Mock()
            mock_serializer.is_valid.return_value = True
            mock_serializer.validated_data = updated_data
            mock_serializer.save.return_value = None
            mock_serializer_class.return_value = mock_serializer
            
            result = ReviewService.update_review(
                self.user, 
                self.test_team, 
                updated_data
            )
            
            self.assertTrue(result['success'])
            self.assertIn('review', result)
            self.assertEqual(result['message'], 'Team review updated successfully')
        
    @patch('interactions.services.reviews.review_service.ReviewCreateUpdateSerializer')
    def test_update_review_invalid_data(self, mock_serializer_class):
        """Test update_review with invalid data"""
        # Create a review first
        content_type = ContentType.objects.get_for_model(self.test_team)
        Review.objects.create(
            user=self.user,
            record_type=content_type,
            record_id=self.test_team.id,
            rating=3,
            description='Initial review'
        )
        
        mock_serializer = Mock()
        mock_serializer.is_valid.return_value = False
        mock_serializer.errors = {'rating': ['Rating must be between 1 and 5']}
        mock_serializer_class.return_value = mock_serializer
        
        result = ReviewService.update_review(
            self.user, 
            self.test_team, 
            self.invalid_review_data
        )
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], {'rating': ['Rating must be between 1 and 5']})
        
    def test_delete_review_unauthenticated_user(self):
        """Test delete_review with unauthenticated user"""
        result = ReviewService.delete_review(self.anonymous_user, self.test_team)
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'Authentication required')
        
    def test_delete_review_not_found(self):
        """Test delete_review when user has no review to delete"""
        result = ReviewService.delete_review(self.user, self.test_team)
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'Review not found')
        
    def test_delete_review_success(self):
        """Test successful review deletion"""
        # Create a review first
        content_type = ContentType.objects.get_for_model(self.test_team)
        review = Review.objects.create(
            user=self.user,
            record_type=content_type,
            record_id=self.test_team.id,
            rating=4,
            description='Review to be deleted'
        )
        
        result = ReviewService.delete_review(self.user, self.test_team)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'Team review deleted successfully')
        
        # Verify review was deleted from database
        self.assertFalse(
            Review.objects.filter(
                user=self.user,
                record_type=content_type,
                record_id=self.test_team.id
            ).exists()
        )
        
    @patch('interactions.services.reviews.review_service.Review.objects.get')
    def test_delete_review_database_error(self, mock_get):
        """Test delete_review when database error occurs"""
        mock_review = Mock()
        mock_review.delete.side_effect = Exception('Database error')
        mock_get.return_value = mock_review
        
        result = ReviewService.delete_review(self.user, self.test_team)
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'Database error')


if __name__ == '__main__':
    unittest.main() 