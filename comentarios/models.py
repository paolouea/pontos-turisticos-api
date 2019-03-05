from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    aprovado = models.BooleanField()

    def __str__(self):
        return "Comentário do " + self.usuario.username
