from django.db import models
from servidor import Servidor
from veiculo import Veiculo


class Emprestimo(models.Model):
    dt_saida = models.DateTimeField()
    dt_devolucao = models.DateTimeField()
    observacao = models.TextField()
    condutor = models.IntegerField()
    servidor = models.ForeignKey(Servidor)
    veiculo = models.ForeignKey(Veiculo)

    class Meta:
        app_label = 'app_frota'