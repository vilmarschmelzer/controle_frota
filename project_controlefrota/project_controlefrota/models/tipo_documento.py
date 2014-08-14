from django.db import models

class Tipo_documento(models.Model):
	nome = models.CharField(max_length=100)