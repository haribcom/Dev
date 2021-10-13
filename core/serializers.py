import logging
from django.contrib.auth import get_user_model
from rest_framework import serializers

LOGGER = logging.getLogger(__name__)


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer class for User Profile
    """

    class Meta:
        """
        Customized fields for user profile
        """
        model = get_user_model()
        fields = ('url', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = get_user_model()(**validated_data)
        user.username = validated_data.get('email')
        user.set_password(password)
        user.save()
        return user
