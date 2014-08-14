from django.db import models
from servidor import Servidor
from chefia import Chefia

class Autorizacao(models.Model):
	cnh = models.CharField(max_length=100)
    dt_inicio = models.DateField()
    dt_fim = models.DateField()
    observacao = models.TextField()
	aprovado = models.BooleanField()
    fk_chefia = models.ForeignKey(Chefia)
    fk_servidor = models.ForeignKey(servidor)