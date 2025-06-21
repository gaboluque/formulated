from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework import viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user"""
    try:
        data = request.data
        email = data.get('email', '').strip()
        password = data.get('password', '')
        username = data.get('username', '').strip()
        
        # Validation
        if not email or not password:
            return Response(
                {'error': 'Email and password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {'error': 'Please enter a valid email address'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Use email as username if username not provided
        if not username:
            username = email
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'An account with this email already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Auto login after registration
        login(request, user)
        
        return Response({
            'message': 'Registration successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': 'Registration failed. Please try again.'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Login user"""
    try:
        data = request.data
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return Response(
                {'error': 'Email and password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Try to find user by email
        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid email or password'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Authenticate
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return Response({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid email or password'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
    except Exception as e:
        return Response(
            {'error': 'Login failed. Please try again.'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def logout_user(request):
    """Logout user"""
    try:
        logout(request)
        return Response(
            {'message': 'Logout successful'}, 
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': 'Logout failed'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def current_user(request):
    """Get current authenticated user"""
    if request.user.is_authenticated:
        return Response({
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': 'Not authenticated'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def csrf_token(request):
    """Get CSRF token for the client"""
    from django.middleware.csrf import get_token
    token = get_token(request)
    return Response({'csrfToken': token}, status=status.HTTP_200_OK) 