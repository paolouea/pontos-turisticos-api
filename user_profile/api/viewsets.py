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

    # Metodo cria o usuário, o perfil do usuário e guarda
    # quem indicou o usuário para o sistema. Valida email único,
    # username unico e garante que quem indicou seja usuário
    # registrado na base, ou nem permite o cadastro.
    def create(self, request, *args, **kwargs):
        user = User()
        user_profile = UserProfile()
        upline_user = User()

        # Pega os dados enviados no post
        user.username = self.request.data["username"]
        user.email = self.request.data["email"]
        user.password = self.request.data["senha"]
        user_profile.cidade = self.request.data["cidade"]
        user_profile.estado = self.request.data["estado"]
        upline = self.request.data["upline"]

        # Verifica se upline existe na base
        try:
            upline_user = User.objects.get_by_natural_key(upline)

        except User.DoesNotExist:
            return Response("Upline não existe", status=status.HTTP_404_NOT_FOUND)

        user_profile.upline = upline_user.username

        # verifica se email já foi cadastrado na base
        try:
            user = User.objects.get(email=user.email)
            return Response("Email em uso. Escolha outro!",
                            status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=user.username)
                return Response("username em uso. Escolha outro!",
                                status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                user = User.objects.create_user(username=user.username,
                                                email=user.email, password=user.password)
                user_profile.user = user
                user_profile.save()
                serializer = UserProfileSerializer(user_profile)
                return Response(serializer.data, status=status.HTTP_201_CREATED)









