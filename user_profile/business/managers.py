from django.contrib.auth.models import User
from ..models import UserProfile


class BusinessException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class UserProfileManager:

    # Metodo que busca todas as primeiras linhas de um determinado usuário
    @staticmethod
    def get_direct_downlines(pk):
        """
        Método com regra negócio para listar primeira linha de um Usuário do sistema
        :param pk:
        :return: Lista de Profiles
        :except: BusinessException com mensagem de erro
        """
        user_profile = UserProfile()
        user = User()
        try:
            user_profile = UserProfile.objects.get(pk=pk)
        except User.DoesNotExist:
            raise BusinessException("Usuário não encontrado no banco")

        try:
            profiles = UserProfile.objects.filter(upline=user_profile.user.username)
            if len(profiles) == 0:
                raise BusinessException("Esse usuário não indicou ninguém")
        except Exception:
            raise BusinessException("Esse usuário não indicou ninguém")

        return profiles
