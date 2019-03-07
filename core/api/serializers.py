from rest_framework.serializers import ModelSerializer, SerializerMethodField
from core.models import PontoTuristico, DocIdentificacao
from comentarios.models import Comentario
from avaliacoes.models import Avaliacao
from atracoes.models import Atracao
from enderecos.models import Endereco
from atracoes.api.serializers import AtracaoSerializer
from enderecos.api.serializers import EnderecoSerializer
from comentarios.api.serializers import ComentarioSerializer
from avaliacoes.api.serializers import AvaliacaoSerializer


class DocIdentificacaoSerializer(ModelSerializer):
    class Meta:
        model = DocIdentificacao
        fields = ("id", "descricao",)


class PontoTuristicoSerializer(ModelSerializer):
    atracoes = AtracaoSerializer(many=True, required=False)
    comentarios = ComentarioSerializer(many=True, required=False)
    avaliacaoes = AvaliacaoSerializer(many=True, required=False)
    endereco = EnderecoSerializer(required=False)
    docIdentificacao = DocIdentificacaoSerializer()

    # Para colocar informacoes calculadas ou que não estejam no MODEL usamos
    # SerializerMethodField. É preciso que o método tenha o nome do campo
    # iniciado pelo prefixo get_nome_do_campo(self, obj)
    # Exemplo mostra descricao completa = titulo + descricao
    descricao_completa = SerializerMethodField()


    class Meta:
        model = PontoTuristico
        fields = ("id", "nome", "descricao", "aprovado", "photo",
                  "atracoes", "comentarios", "avaliacaoes", "endereco",
                  "docIdentificacao", "descricao_completa", "exemplo_regra_neg")

    def create(self, validated_data):

        # Armazer as relações em listas separadas, copiadas por valor,
        # Para sem processadas e salvas separadamente
        avalicao_flag = False
        atracao_flag = False
        comentario_flag = False
        endereco_flag = False
        doc_flag = False
        lista_de_atracoes = []
        lista_de_comentarios = []
        lista_de_avalicoes = []
        endereco = ""
        end = ""
        docId = None
        doc = None

        if "endereco" in validated_data:
            endereco = validated_data["endereco"]
            endereco_flag = True
            del validated_data["endereco"]

        if "atracoes" in validated_data:
            lista_de_atracoes = validated_data["atracoes"]
            atracao_flag = True
            del validated_data["atracoes"]

        if "comentarios" in validated_data:
            lista_de_comentarios = validated_data["comentarios"]
            comentario_flag = True
            del validated_data["comentarios"]

        if "avaliacaoes" in validated_data:
            lista_de_avalicoes = validated_data["avaliacaoes"]
            avalicao_flag = True
            del validated_data["avaliacaoes"]

        if "docIdentificacao" in validated_data:
            docId = validated_data["docIdentificacao"]
            doc_flag = True
            del validated_data["docIdentificacao"]

        # Remove as relacoes de dentro do mapa para poder salvar
        # pontos turisticos pelo metodo direto do framework
        # if atracao_flag:
        #     del validated_data["atracoes"]
        # if comentario_flag:
        #     del validated_data["comentarios"]
        # if avalicao_flag:
        #     del validated_data["avaliacaoes"]
        # if endereco_flag:
        #     del validated_data["endereco"]
        #     print("Endereco removido do validated...")

        #salva ponto turistico
        pontoTuristico = PontoTuristico.objects.create(**validated_data)
        if atracao_flag:
            self.cria_atracoes(lista_de_atracoes, pontoTuristico)
        if comentario_flag:
            self.cria_comentarios(lista_de_comentarios, pontoTuristico)
        if avalicao_flag:
            self.cria_avaliacoes(lista_de_avalicoes, pontoTuristico)
        if endereco_flag:
            end = Endereco.objects.create(**endereco)
            pontoTuristico.endereco = end
        if doc_flag:
            doc = DocIdentificacao.objects.create(**docId)
            pontoTuristico.docIdentificacao = doc

        pontoTuristico.save()
        return pontoTuristico

    def cria_atracoes(self, atracoes, pontoTuristico):
        for atracao in atracoes:
            at = Atracao.objects.create(**atracao)
            pontoTuristico.atracoes.add(at)

    def cria_comentarios(self, comentarios, pontoTuristico):
        for comentario in comentarios:
            com = Comentario.objects.create(**comentario)
            pontoTuristico.comentarios.add(com)

    def cria_avaliacoes(self, avaliacoes, pontoTuristico):
        for avaliacao in avaliacoes:
            av = Avaliacao.objects.create(**avaliacao)
            pontoTuristico.avaliacaoes.add(av)

    # obj representa o modelo que está sendo tratado nesse serializer
    def get_descricao_completa(self, obj):
        return "%s - %s" % (obj.nome, obj.descricao)