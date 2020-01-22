from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.main.views import UserProfileViewSet

app_name = 'main'

router = DefaultRouter()
router.register(r'user_profile', UserProfileViewSet, basename='user_profile')

urlpatterns = [
    path('v1/', include(router.urls)),
]