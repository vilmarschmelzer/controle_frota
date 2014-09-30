from django.db import models
from app_frota.models import Cidade


class Rota(models.Model):
    cidade_origem = models.ForeignKey(Cidade, related_name='cidade_origem_rota')
    cidade_destino = models.ForeignKey(Cidade, related_name='cidade_destino_rota')
    endereco_origem = models.CharField(max_length=200)
    endereco_destino = models.CharField(max_length=200)

    class Meta:
        app_label = 'app_frota'