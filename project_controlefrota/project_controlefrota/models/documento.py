from django.db import models
from tipo_documento import Tipo_documento
from veiculo import Veiculo

class Documento(models.Model):
	numero = models.CharField(max_length=100)
	dt_vig_inicio = models.DateField(null=True)
	dt_vig_fim = models.DateField(null=True)
	fk_tipo_documento = models.ForeignKey(Tipo_documento)
	fk_veiculo = models.ForeignKey(Veiculo)