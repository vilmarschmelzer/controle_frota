from django.db import models
from marca import Marca


class Veiculo(models.Model):
    chassis = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca)
    modelo = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    placa = models.CharField(max_length=100)

    def get_veiculos_disponiveis(self, dt_saida, dt_devolucao, not_id=0):
        veiculos = Veiculo.objects.raw('select id from app_frota_veiculo where id not in '
                                       +'(select a.id as id from app_frota_veiculo a '
                                       +'inner join app_frota_emprestimo b on (a.id=b.veiculo_id) '
                                        'where not b.dt_saida between \'%s\' and \'%s\' and not b.id=%s)'
                                       % (dt_saida, dt_devolucao, not_id))

        return veiculos

    def __unicode__(self):
        return self.nome

    class Meta:
        app_label = 'app_frota'