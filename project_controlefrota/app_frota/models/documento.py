from django.db import models
from tipo_documento import TipoDocumento
from veiculo import Veiculo


class Documento(models.Model):
    numero = models.CharField(max_length=100)
    dt_vig_inicio = models.DateField(null=True)
    dt_vig_fim = models.DateField(null=True)
    tipo_documento = models.ForeignKey(TipoDocumento)
    veiculo = models.ForeignKey(Veiculo)

    class Meta:
        app_label = 'app_frota'