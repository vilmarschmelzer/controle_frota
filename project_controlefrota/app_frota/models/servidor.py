from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


class Servidor(User):
    cpf = models.CharField(max_length=11, unique=True)

    def is_conduzir(self, id=None):
        from app_frota.models import Autorizacao
        if id is None:
            id = self.id
        auto = Autorizacao.objects.raw('select id from app_frota_autorizacao where \'%s\' between dt_inicio and dt_fim and servidor_id=%s limit 1' % (str(datetime.now().date() ), str(id)))

        return len(list(auto)) > 0

    def __unicode__(self):
        return (self.first_name+' '+self.last_name)

    class Meta:
        app_label = 'app_frota'