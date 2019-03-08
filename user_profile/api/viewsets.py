from rest_framework.viewsets import ModelViewSet
from ..models import UserProfile
from .serializers import UserProfileSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status

class UserProfileViewSet(ModelViewSet):
    """
    ViewSet for UserProfile
    """
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def create(self, request, *args, **kwargs):
        user = User()
        user_profile = UserProfile()

        # Pega os dados enviados no post
        user.username = self.request.data["username"]
        user.email = self.request.data["email"]
        user.password = self.request.data["senha"]
        user_profile.cidade = self.request.data["cidade"]
        user_profile.estado = self.request.data["estado"]
        upline = self.request.data["upline"]

        user = User.objects.create_user(username=user.username,
                                        email=user.email, password=user.password)

        upline_user = User.objects.get_by_natural_key(upline)
        user_profile.user = user
        user_profile.upline = upline_user.username
        user_profile.save()

        serializer = UserProfileSerializer(user_profile)

        return Response(serializer.data, status=status.HTTP_201_CREATED)






