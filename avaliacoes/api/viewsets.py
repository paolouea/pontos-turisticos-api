from rest_framework import viewsets
from .serializers import AvaliacaoSerializer
from ..models import Avaliacao


class AvaliacaoViewSet(viewsets.ModelViewSet):

    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
