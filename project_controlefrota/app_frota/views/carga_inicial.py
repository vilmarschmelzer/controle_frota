# coding:utf-8
from django.shortcuts import redirect
from django.contrib.auth.models import Group, User
from app_frota.models import Administrador
from django.db import transaction
from django.conf import settings


@transaction.commit_on_success
def carga(request):

    grupos_nome = ['Administrador', 'Servidor']

    for gp_nome in grupos_nome:
        gp = Group.objects.filter(name=gp_nome)

        if len(gp) == 0:
            gp = Group(name=gp_nome)
            gp.save()

    cpf = '06885813907'

    adm = Administrador.objects.filter(cpf=cpf)

    if len(adm) == 0:

        adm = Administrador()

        adm.cpf = cpf
        adm.first_name = 'Admin'
        adm.email = 'admin@teste.com'
        adm.username = adm.email
        adm.is_superuser = True
        adm.set_password('teste')

        adm.save()

        gp = Group.objects.get(name=grupos_nome[0])
        User(adm.id).groups.add(gp.id)

    return redirect('/')