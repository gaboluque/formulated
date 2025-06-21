from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from teams.models import Team, Member
from teams.serializers import TeamSerializer, MemberSerializer
from interactions.serializers import LikeCreateSerializer, ReviewSerializer, ReviewCreateUpdateSerializer
from interactions.services.likes.like_service import LikeService
from interactions.services.reviews.review_service import ReviewService


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all().order_by('name')
    serializer_class = TeamSerializer
    
    @action(detail=True, methods=['get', 'post', 'delete'], url_path='likes', url_name='likes', serializer_class=LikeCreateSerializer)
    def likes(self, request, pk=None):
        """
        GET: Check if current user likes this team
        POST: Like this team
        DELETE: Unlike this team
        """
        team = self.get_object()
        
        if request.method == 'GET':
            result = LikeService.check_like(request.user, team)
            if result['success']:
                return Response({'liked': result['liked']}, status=status.HTTP_200_OK)
            else:
                return Response({'error': result['error']}, status=status.HTTP_401_UNAUTHORIZED)
        
        elif request.method == 'POST':
            result = LikeService.create_like(request.user, team)
            if result['success']:
                return Response(result['like'], status=status.HTTP_201_CREATED)
            else:
                return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            result = LikeService.remove_like(request.user, team)
            if result['success']:
                return Response({'liked': False}, status=status.HTTP_204_NO_CONTENT)
            else:
                error_status = status.HTTP_401_UNAUTHORIZED if 'Authentication required' in result['error'] else status.HTTP_404_NOT_FOUND
                return Response({'error': result['error']}, status=error_status)
    
    @action(detail=True, methods=['get', 'post', 'put', 'delete'], url_path='reviews', url_name='reviews', serializer_class=ReviewCreateUpdateSerializer)
    def reviews(self, request, pk=None):
        """
        GET: Get all reviews for this team
        POST: Create a review for this team
        PUT: Update current user's review for this team
        DELETE: Delete current user's review for this team
        """
        team = self.get_object()
        
        if request.method == 'GET':
            result = ReviewService.get_reviews_for_object(team)
            return Response(result['reviews'], status=status.HTTP_200_OK)
        
        elif request.method == 'POST':
            result = ReviewService.create_review(request.user, team, request.data)
            if result['success']:
                return Response(result['review'], status=status.HTTP_201_CREATED)
            else:
                error_status = status.HTTP_401_UNAUTHORIZED if 'Authentication required' in result['error'] else status.HTTP_400_BAD_REQUEST
                return Response({'error': result['error']}, status=error_status)
        
        elif request.method == 'PUT':
            result = ReviewService.update_review(request.user, team, request.data)
            if result['success']:
                return Response(result['review'], status=status.HTTP_200_OK)
            else:
                error_status = status.HTTP_401_UNAUTHORIZED if 'Authentication required' in result['error'] else status.HTTP_404_NOT_FOUND
                return Response({'error': result['error']}, status=error_status)
        
        elif request.method == 'DELETE':
            result = ReviewService.delete_review(request.user, team)
            if result['success']:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                error_status = status.HTTP_401_UNAUTHORIZED if 'Authentication required' in result['error'] else status.HTTP_404_NOT_FOUND
                return Response({'error': result['error']}, status=error_status)
    
    def get_serializer_class(self):
        """Return the appropriate serializer class based on the action"""
        if self.action == 'reviews':
            if self.request.method in ['POST', 'PUT']:
                return ReviewCreateUpdateSerializer
            else:
                return ReviewSerializer
        return super().get_serializer_class()


class MemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Member.objects.all().order_by('name')
    serializer_class = MemberSerializer
    
    @action(detail=True, methods=['get', 'post', 'delete'], url_path='likes', url_name='likes', serializer_class=LikeCreateSerializer)
    def likes(self, request, pk=None):
        """
        GET: Check if current user likes this member
        POST: Like this member
        DELETE: Unlike this member
        """
        member = self.get_object()
        
        if request.method == 'GET':
            result = LikeService.check_like(request.user, member)
            if result['success']:
                return Response({'liked': result['liked']}, status=status.HTTP_200_OK)
            else:
                return Response({'error': result['error']}, status=status.HTTP_401_UNAUTHORIZED)
        
        elif request.method == 'POST':
            result = LikeService.create_like(request.user, member)
            if result['success']:
                return Response(result['like'], status=status.HTTP_201_CREATED)
            else:
                return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            result = LikeService.remove_like(request.user, member)
            if result['success']:
                return Response({'liked': False}, status=status.HTTP_204_NO_CONTENT)
            else:
                error_status = status.HTTP_401_UNAUTHORIZED if 'Authentication required' in result['error'] else status.HTTP_404_NOT_FOUND
                return Response({'error': result['error']}, status=error_status)
    
    @action(detail=True, methods=['get', 'post', 'put', 'delete'], url_path='reviews', url_name='reviews', serializer_class=ReviewCreateUpdateSerializer)
    def reviews(self, request, pk=None):
        """
        GET: Get all reviews for this member
        POST: Create a review for this member
        PUT: Update current user's review for this member
        DELETE: Delete current user's review for this member
        """
        member = self.get_object()
        
        if request.method == 'GET':
            result = ReviewService.get_reviews_for_object(member)
            return Response(result['reviews'], status=status.HTTP_200_OK)
        
        elif request.method == 'POST':
            result = ReviewService.create_review(request.user, member, request.data)
            if result['success']:
                return Response(result['review'], status=status.HTTP_201_CREATED)
            else:
                error_status = status.HTTP_401_UNAUTHORIZED if 'Authentication required' in result['error'] else status.HTTP_400_BAD_REQUEST
                return Response({'error': result['error']}, status=error_status)
        
        elif request.method == 'PUT':
            result = ReviewService.update_review(request.user, member, request.data)
            if result['success']:
                return Response(result['review'], status=status.HTTP_200_OK)
            else:
                error_status = status.HTTP_401_UNAUTHORIZED if 'Authentication required' in result['error'] else status.HTTP_404_NOT_FOUND
                return Response({'error': result['error']}, status=error_status)
        
        elif request.method == 'DELETE':
            result = ReviewService.delete_review(request.user, member)
            if result['success']:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                error_status = status.HTTP_401_UNAUTHORIZED if 'Authentication required' in result['error'] else status.HTTP_404_NOT_FOUND
                return Response({'error': result['error']}, status=error_status)
    
    def get_serializer_class(self):
        """Return the appropriate serializer class based on the action"""
        if self.action == 'reviews':
            if self.request.method in ['POST', 'PUT']:
                return ReviewCreateUpdateSerializer
            else:
                return ReviewSerializer
        return super().get_serializer_class()