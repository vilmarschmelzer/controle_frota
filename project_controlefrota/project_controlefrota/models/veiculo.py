from django.db import models

class Veiculo(models.Model):
	chassis = models.CharField(max_length=100)
	marca = models.IntegerField()
	modelo = models.CharField(max_length=100)
	nome = models.CharField(max_length=100)
	placa = models.CharField(max_length=100)