from django.db import models


class Marca(models.Model):
    nome = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nome

    class Meta:
        app_label = 'app_frota'