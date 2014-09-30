from django.db import models
from servidor import Servidor


class Autorizacao(models.Model):
    cnh = models.CharField(max_length=100)
    dt_inicio = models.DateField()
    dt_fim = models.DateField()
    observacao = models.TextField()
    aprovado = models.NullBooleanField()
    servidor = models.ForeignKey(Servidor)

    class Meta:
        app_label = 'app_frota'