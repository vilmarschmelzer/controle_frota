from django.db import models


class Estado(models.Model):
    abreviado = models.CharField(max_length=10)
    nome = models.CharField(max_length=200)

    def __unicode__(self):
        return self.abreviado

    class Meta:
        app_label = 'app_frota'