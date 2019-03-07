from django.db import models
from atracoes.models import Atracao
from comentarios.models import Comentario
from avaliacoes.models import Avaliacao
from enderecos.models import Endereco
# Create your models here.


class DocIdentificacao(models.Model):
    descricao = models.CharField(max_length=50)

    def __str__(self):
        return self.descricao


class PontoTuristico(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField()
    aprovado = models.BooleanField(default=False)
    atracoes = models.ManyToManyField(Atracao)
    comentarios = models.ManyToManyField(Comentario)
    avaliacaoes = models.ManyToManyField(Avaliacao)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to='pontos_turisticos', null=True, blank=True)
    docIdentificacao = models.OneToOneField(DocIdentificacao, on_delete=models.CASCADE,
                                            null=True, blank=True)

    def __str__(self):
        return self.nome

    # Metodo de regra de negocio que se comporta como campo do model
    # Coloca nos fields da serializer com o mesmo nome do metodo aqui
    @property
    def exemplo_regra_neg(self):
        return "Regra de Negocio de Dentro do Model: %s" % (self)