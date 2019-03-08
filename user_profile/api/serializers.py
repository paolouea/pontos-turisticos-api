from rest_framework.serializers import ModelSerializer
from ..models import UserProfile
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email",)


class UserProfileSerializer(ModelSerializer):

    user = UserSerializer(required=False)

    class Meta:
        model = UserProfile
        fields = ("id", "user", "upline", "cidade", "estado",)




