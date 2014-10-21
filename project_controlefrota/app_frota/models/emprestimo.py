from django.db import models
from servidor import Servidor
from veiculo import Veiculo
from rota import Rota


class Emprestimo(models.Model):
    dt_saida = models.DateTimeField()
    dt_devolucao = models.DateTimeField()
    observacao = models.TextField()
    condutor = models.ForeignKey(Servidor, null=True, related_name='emprestimo_condutor')
    servidor = models.ForeignKey(Servidor, related_name='emprestimo_servidor')
    veiculo = models.ForeignKey(Veiculo, null=True)
    rota = models.ForeignKey(Rota)
    aprovado = models.NullBooleanField()

    class Meta:
        app_label = 'app_frota'