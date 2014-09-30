from django.db import models
from servidor import Servidor


class Autorizacao(models.Model):
    cnh = models.CharField(max_length=100)
    dt_inicio = models.DateField(auto_now=True)
    dt_fim = models.DateField(null=True)
    observacao = models.TextField()
    aprovado = models.NullBooleanField(null=True)
    servidor = models.ForeignKey(Servidor)

    class Meta:
        app_label = 'app_frota'