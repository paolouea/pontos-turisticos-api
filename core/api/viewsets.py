from rest_framework import viewsets
from core.models import PontoTuristico, DocIdentificacao
from atracoes.models import Atracao
from core.api.serializers import PontoTuristicoSerializer, DocIdentificacaoSerializer
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response


class DocIdentificacaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for DocIdentificacao
    """
    serializer_class = DocIdentificacaoSerializer
    queryset = DocIdentificacao.objects.all()

class PontoTuristicosViewSet(viewsets.ModelViewSet):
    """
    ViewSet for PontoTuristicos
    """
    # Sobrescrever o método get_queryset() para fazer uma
    # busca personalizada.
    # queryset = PontoTuristico.objects.all()
    serializer_class = PontoTuristicoSerializer
    filter_backends = (SearchFilter, )
    search_fields = ("nome", "descricao", "endereco__linha1")
    # Django Permitions ja prove toda a parte de controle de acesso
    # e permissões aos usuários, de maneira individual ou em
    # grupos de usuários. Essas permissões podem ser editadas
    # pelo painel adm do django
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    # Sobrescrevendo o método queryset
    def get_queryset(self):

        id = self.request.query_params.get("id", None)
        nome = self.request.query_params.get("nome", None)
        descricao = self.request.query_params.get("descricao", None)

        queryset = PontoTuristico.objects.all()
        if id:
            queryset = PontoTuristico.objects.filter(pk=id)
        if nome:
            #print(nome)
            queryset = queryset.filter(nome__iexact=nome)
        if descricao:
            queryset = queryset.filter(descricao__iexact=descricao)
        return queryset

    # Sobrescrevendo o metodo list() - bind com metodo GET do request
    def list(self, request, *args, **kwargs):
        return super(PontoTuristicosViewSet, self).list(request, *args, **kwargs)

    # Sobrescrevendo o metodo create - bind com metodo POST do request
    def create(self, request, *args, **kwargs):
        return super(PontoTuristicosViewSet, self).create(request, *args, **kwargs)

    # Sobrescrever o metodo destroy() - bind com metodo DELETE do request
    # fazer log de exclusão
    # verificar permissões de exclusão e etc.
    def destroy(self, request, *args, **kwargs):
        return super(PontoTuristicosViewSet, self).destroy(request, *args, **kwargs)

    # Actions personalizadas quando os elementos do crud não cobrem
    # methods lista de metodos e detail= se acessa o endpoint ou recurso dele
    # para acessar localhost:8000/pontosturisticos/1/denunciar
    @action(methods=['GET'], detail=True)
    def denunciar(self, request, pk=None):
        pass

    #Com deital false, o acesso é feito ao endpoint
    #localhost:8000/pontosturiticos/
    @action(methods=['GET'], detail=False)
    def teste(self, request, pk=None):
        pass

    @action(methods=["POST"], detail=True)
    def associa_atracao_ponto(self, request, pk):
        id_atracoes = request.data["ids"]
        ponto = PontoTuristico.objects.get(pk=pk)

        for id in id_atracoes:
            ponto.atracoes.add(Atracao.objects.get(pk=id))

        ponto.save()
        return Response("ok")