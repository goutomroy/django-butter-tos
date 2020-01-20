from django.contrib.auth.models import User
from rest_framework import serializers
from apps.main.models import UserProfile
from apps.tos.models import TermsOfService, UserTermsOfService


class TermsOfServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = TermsOfService
        fields = ('id', 'slug', 'name', 'version_number', 'status', 'activation_date')


class UserTermsOfServiceSerializer(serializers.ModelSerializer):

    terms = TermsOfServiceSerializer()

    class Meta:
        model = UserTermsOfService
        fields = ('id', 'terms')