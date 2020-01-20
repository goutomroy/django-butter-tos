from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.tos.views import TermsOfServiceViewSet, UserTermsOfServiceViewSet

app_name = 'tos'

router = DefaultRouter()
router.register(r'terms_of_services', TermsOfServiceViewSet, basename='terms_of_service')
router.register(r'user_terms_of_services', UserTermsOfServiceViewSet, basename='user_terms_of_service')

urlpatterns = [
    path('v1/', include(router.urls)),
]