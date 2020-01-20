from django.contrib.auth.models import User
from rest_framework import serializers
from apps.main.models import UserProfile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'street', 'postal_code')
