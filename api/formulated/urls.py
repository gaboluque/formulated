from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from teams.views import TeamViewSet, MemberViewSet
from races.views import CircuitViewSet, RaceViewSet, PositionViewSet
from .auth_views import register, login_user, logout_user, current_user, csrf_token, UserViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'members', MemberViewSet)
router.register(r'circuits', CircuitViewSet)
router.register(r'races', RaceViewSet)
router.register(r'positions', PositionViewSet)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # Auth endpoints
    path('api/auth/register/', register, name='register'),
    path('api/auth/login/', login_user, name='login'),
    path('api/auth/logout/', logout_user, name='logout'),
    path('api/auth/me/', current_user, name='current_user'),
    path('api/auth/csrf/', csrf_token, name='csrf_token'),
]
