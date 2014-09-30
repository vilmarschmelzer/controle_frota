# coding:utf-8
from django.shortcuts import redirect
from django.contrib.auth.models import Group, User
from app_frota.models import Administrador, Marca
from django.db import transaction


@transaction.commit_on_success
def carga(request):

    grupos_nome = ['Administrador', 'Servidor', 'Chefia']

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

    nome_marcas = ['Volkswagen', 'Chevrolet', 'Toyota',  'Ford', 'Fiat', 'Renault', 'Mercedez', 'Hyundai', 'Mazda', 'Nissan']

    for marca_nome in nome_marcas:
        marca = Marca.objects.filter(nome=marca_nome)

        if len(marca) == 0:
            marca = Marca(nome=marca_nome)
            marca.save()


    return redirect('/')