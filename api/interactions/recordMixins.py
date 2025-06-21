from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from interactions.models import Like
from interactions.serializers import LikeSerializer, LikeCreateSerializer, ReviewSerializer, ReviewCreateUpdateSerializer
from interactions.services.likes.like_service import LikeService
from interactions.services.reviews.review_service import ReviewService

class RecordMixin:
    """
    Mixin to add likes and reviews to a record
    """

    @action(detail=True, methods=['get', 'post', 'delete'], url_path='likes', url_name='likes', serializer_class=LikeCreateSerializer)
    def likes(self, request, pk=None):
        """
        GET: Check if current user likes this object
        POST: Like this object
        DELETE: Unlike this object
        """
        object = self.get_object()
        
        if request.method == 'GET':
            result = LikeService.check_like(request.user, object)
            if result['success']:
                return Response({'liked': result['liked']}, status=status.HTTP_200_OK)
            else:
                return Response({'error': result['error']}, status=status.HTTP_401_UNAUTHORIZED)
        
        elif request.method == 'POST':
            result = LikeService.create_like(request.user, object)
            if result['success']:
                return Response(result['like'], status=status.HTTP_201_CREATED)
            else:
                return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            result = LikeService.remove_like(request.user, object)
            if result['success']:
                return Response({'liked': False}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': result['error']}, status=status.HTTP_401_UNAUTHORIZED)
            
    def get_serializer_class(self):
        """Return the appropriate serializer class based on the action"""
        if self.action == 'likes':
            return LikeCreateSerializer
        return super().get_serializer_class()
            
    
    @action(detail=True, methods=['get', 'post', 'put', 'delete'], url_path='reviews', url_name='reviews', serializer_class=ReviewCreateUpdateSerializer)
    def reviews(self, request, pk=None):
        """
        GET: Get all reviews for this object
        POST: Create a review for this object
        PUT: Update current user's review for this object
        DELETE: Delete current user's review for this object
        """
        object = self.get_object()
        
        if request.method == 'GET':
            result = ReviewService.get_reviews_for_object(object)
            return Response(result['reviews'], status=status.HTTP_200_OK)
        
        elif request.method == 'POST':
            result = ReviewService.create_review(request.user, object, request.data)
            if result['success']:
                return Response(result['review'], status=status.HTTP_201_CREATED)
            else:
                return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'PUT':
            result = ReviewService.update_review(request.user, object, request.data)
            if result['success']:
                return Response(result['review'], status=status.HTTP_200_OK)
            else:
                return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)
            
        elif request.method == 'DELETE':
            result = ReviewService.delete_review(request.user, object)
            if result['success']:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)
            
    def get_serializer_class(self):
        """Return the appropriate serializer class based on the action"""
        if self.action == 'reviews':
            if self.request.method in ['POST', 'PUT']:
                return ReviewCreateUpdateSerializer
            else:
                return ReviewSerializer
        return super().get_serializer_class()