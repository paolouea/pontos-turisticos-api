from rest_framework import viewsets
from ..models import Atracao
from .serializers import AtracaoSerializer


class AtracaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Atrações
    """
    queryset = Atracao.objects.all()
    serializer_class = AtracaoSerializer
    filter_fields = ("nome",)
