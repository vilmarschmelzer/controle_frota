from django.db import models
from marca import Marca


class Veiculo(models.Model):
    chassis = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca)
    modelo = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    placa = models.CharField(max_length=100)

    class Meta:
        app_label = 'app_frota'