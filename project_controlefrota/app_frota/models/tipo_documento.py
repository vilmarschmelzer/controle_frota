from django.db import models


class TipoDocumento(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        app_label = 'app_frota'