
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from races.models import Circuit, Race, Position
from races.serializers import CircuitSerializer, RaceSerializer, PositionSerializer
from interactions.services.likes.like_service import LikeService
from interactions.services.reviews.review_service import ReviewService
from interactions.serializers import LikeCreateSerializer, ReviewSerializer, ReviewCreateUpdateSerializer

class CircuitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Circuit.objects.all().order_by('name')
    serializer_class = CircuitSerializer
    
    @action(detail=True, methods=['get', 'post', 'delete'], url_path='likes', url_name='likes', serializer_class=LikeCreateSerializer)
    def likes(self, request, pk=None):
        """
        GET: Check if current user likes this circuit
        POST: Like this circuit
        DELETE: Unlike this circuit
        """
        circuit = self.get_object()
        
        if request.method == 'GET':
            result = LikeService.check_like(request.user, circuit)
            if result['success']:
                return Response({'liked': result['liked']}, status=status.HTTP_200_OK)
            else:
                return Response({'error': result['error']}, status=status.HTTP_401_UNAUTHORIZED)
        
        elif request.method == 'POST':
            result = LikeService.create_like(request.user, circuit)
            if result['success']:
                return Response(result['like'], status=status.HTTP_201_CREATED)
            else:
                return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            result = LikeService.remove_like(request.user, circuit)
            if result['success']:
                return Response({'liked': False}, status=status.HTTP_204_NO_CONTENT)
            else:
                error_status = status.HTTP_401_UNAUTHORIZED if 'Authentication required' in result['error'] else status.HTTP_404_NOT_FOUND
                return Response({'error': result['error']}, status=error_status)
    
    @action(detail=True, methods=['get', 'post', 'put', 'delete'], url_path='reviews', url_name='reviews', serializer_class=ReviewCreateUpdateSerializer)
    def reviews(self, request, pk=None):
        """
        GET: Get all reviews for this circuit
        POST: Create a review for this circuit
        PUT: Update current user's review for this circuit
        DELETE: Delete current user's review for this circuit
        """
        circuit = self.get_object()
        
        if request.method == 'GET':
            result = ReviewService.get_reviews_for_object(circuit)
            return Response(result['reviews'], status=status.HTTP_200_OK)
        
        elif request.method == 'POST':
            result = ReviewService.create_review(request.user, circuit, request.data)
            if result['success']:
                return Response(result['review'], status=status.HTTP_201_CREATED)
            else:
                error_status = status.HTTP_401_UNAUTHORIZED if 'Authentication required' in result['error'] else status.HTTP_400_BAD_REQUEST
                return Response({'error': result['error']}, status=error_status)
        
        elif request.method == 'PUT':
            result = ReviewService.update_review(request.user, circuit, request.data)
            if result['success']:
                return Response(result['review'], status=status.HTTP_200_OK)
            else:
                error_status = status.HTTP_401_UNAUTHORIZED if 'Authentication required' in result['error'] else status.HTTP_404_NOT_FOUND
                return Response({'error': result['error']}, status=error_status)
        
        elif request.method == 'DELETE':
            result = ReviewService.delete_review(request.user, circuit)
            if result['success']:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                error_status = status.HTTP_401_UNAUTHORIZED if 'Authentication required' in result['error'] else status.HTTP_404_NOT_FOUND
                return Response({'error': result['error']}, status=error_status)
    

class RaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Race.objects.all().order_by('start_at')
    serializer_class = RaceSerializer
    
    @action(detail=True, methods=['get', 'post', 'delete'], url_path='likes', url_name='likes', serializer_class=LikeCreateSerializer)
    def likes(self, request, pk=None):
        """
        GET: Check if current user likes this race
        POST: Like this race
        DELETE: Unlike this race
        """
        race = self.get_object()
        
        if request.method == 'GET':
            result = LikeService.check_like(request.user, race)
            if result['success']:
                return Response({'liked': result['liked']}, status=status.HTTP_200_OK)
            else:
                return Response({'error': result['error']}, status=status.HTTP_401_UNAUTHORIZED)
        
        elif request.method == 'POST':
            result = LikeService.create_like(request.user, race)
            if result['success']:
                return Response(result['like'], status=status.HTTP_201_CREATED)
            else:
                return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            result = LikeService.remove_like(request.user, race)
            if result['success']:
                return Response({'liked': False}, status=status.HTTP_204_NO_CONTENT)
            else:
                error_status = status.HTTP_401_UNAUTHORIZED if 'Authentication required' in result['error'] else status.HTTP_404_NOT_FOUND
                return Response({'error': result['error']}, status=error_status)
    
    @action(detail=True, methods=['get', 'post', 'put', 'delete'], url_path='reviews', url_name='reviews', serializer_class=ReviewCreateUpdateSerializer)
    def reviews(self, request, pk=None):
        """
        GET: Get all reviews for this race
        POST: Create a review for this race
        PUT: Update current user's review for this race
        DELETE: Delete current user's review for this race
        """
        race = self.get_object()
        
        if request.method == 'GET':
            result = ReviewService.get_reviews_for_object(race)
            return Response(result['reviews'], status=status.HTTP_200_OK)
        
        elif request.method == 'POST':
            result = ReviewService.create_review(request.user, race, request.data)
            if result['success']:
                return Response(result['review'], status=status.HTTP_201_CREATED)
            else:
                error_status = status.HTTP_401_UNAUTHORIZED if 'Authentication required' in result['error'] else status.HTTP_400_BAD_REQUEST
                return Response({'error': result['error']}, status=error_status)
        
        elif request.method == 'PUT':
            result = ReviewService.update_review(request.user, race, request.data)
            if result['success']:
                return Response(result['review'], status=status.HTTP_200_OK)
            else:
                error_status = status.HTTP_401_UNAUTHORIZED if 'Authentication required' in result['error'] else status.HTTP_404_NOT_FOUND
                return Response({'error': result['error']}, status=error_status)
        
        elif request.method == 'DELETE':
            result = ReviewService.delete_review(request.user, race)
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


class PositionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Position.objects.all().order_by('race', 'position')
    serializer_class = PositionSerializer
