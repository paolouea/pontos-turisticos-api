from rest_framework.viewsets import ModelViewSet
from ..models import UserProfile
from .serializers import UserProfileSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.filters import SearchFilter
from user_profile.business.managers import UserProfileManager, BusinessException



class UserProfileViewSet(ModelViewSet):
    """
    ViewSet for UserProfile
    """
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    filter_backends = (SearchFilter,)
    filterset_fields = ('upline', )


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

        # Valida se email já foi cadastrado na base
        try:
            user = User.objects.get(email=user.email)
            return Response("Email em uso. Escolha outro!",
                            status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            # Valida se username já existe na base
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


    # Actions personalizadas quando os elementos do crud não cobrem
    # methods lista de metodos e detail= se acessa o endpoint ou recurso dele
    # para acessar localhost:8000/pontosturisticos/1/denunciar
    @action(methods=['GET'], detail=True)
    def show_first_line(self, request, pk=None):
        """
        Mostra os Indicados diretos da rede para um dado Nó
        :param request:
        :param pk:
        :return: Response with Serialized JSON
        """

        try:
            profiles = UserProfileManager.get_direct_downlines(pk=pk)
        except BusinessException as be:
            return Response(be.message, status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=True)
    def show_all_lines(self, request, pk=None):
        """
        Mostra todas as linhas da rede a partir de um nó dado
        :param request:
        :param pk:
        :return: Response - Serialized JSON
        """
        #levels = int(self.request.query_params.get("levels"))

        try:
            profiles = UserProfileManager.get_direct_downlines(pk=pk)

        except BusinessException as be:
            return Response(be.message, status.HTTP_404_NOT_FOUND)

        for profile in profiles:
            try:
                new_qs = UserProfileManager.get_direct_downlines(pk=profile.id)
                profiles = profiles.union(new_qs, all=False)
            except BusinessException:
                pass


        serializer = UserProfileSerializer(profiles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)








