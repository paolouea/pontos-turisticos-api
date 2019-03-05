from rest_framework import viewsets
from core.models import PontoTuristico
from core.api.serializers import PontoTuristicoSerializer


class PontoTuristicosViewSet(viewsets.ModelViewSet):
    """
    ViewSet for PontoTuristicos
    """
    queryset = PontoTuristico.objects.all()
    serializer_class = PontoTuristicoSerializer
