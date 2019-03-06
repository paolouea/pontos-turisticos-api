from rest_framework.serializers import ModelSerializer
from core.models import PontoTuristico
from atracoes.api.serializers import AtracaoSerializer
from enderecos.api.serializers import EnderecoSerializer
from comentarios.api.serializers import ComentarioSerializer
from avaliacoes.api.serializers import AvaliacaoSerializer

class PontoTuristicoSerializer(ModelSerializer):
    atracoes = AtracaoSerializer(many=True)
    endereco = EnderecoSerializer()
    comentarios = ComentarioSerializer(many=True)
    avaliacaoes = AvaliacaoSerializer(many=True)
    class Meta:
        model = PontoTuristico
        fields = ("id", "nome", "descricao", "aprovado", "photo",
                  "atracoes", "comentarios", "avaliacaoes", "endereco")