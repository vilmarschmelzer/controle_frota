from django.db import models
from django.contrib.auth.models import User

class Servidor(User):
    cpf = models.CharField(max_length=100)