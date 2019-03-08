from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    upline = models.CharField(max_length=50)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    created = models.DateTimeField(auto_now_add=True)
