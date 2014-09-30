#coding:utf-8
from django.shortcuts import render, redirect
from app_frota.models import Autorizacao
from decorators.permissoes import group_required
from django.conf import settings
from app_frota.forms.pesquisa import FormPesquisa
from app_frota.forms.autorizacao import FormAutorizacao
from django.db.models import Q
from django.core.paginator import Paginator
from django.db import transaction
from datetime import datetime, timedelta


@group_required(settings.PERM_GRUPO_CHEFIA)
@transaction.commit_on_success
def visualizar(request, id):

    autorizacao = Autorizacao.objects.get(pk=id)

    if request.method == 'POST':
        if 'aprovado' in request.POST:
            if request.POST['aprovado'] == 'True':
                autorizacao.aprovado = True
            else:
                autorizacao.aprovado = False

            autorizacao.save()

        return redirect('/consultar-autorizacoes/')

    return render(request, 'autorizacao/visualizar.html', {'autorizacao': autorizacao })


@group_required(settings.PERM_GRUPO_CHEFIA)
def consultar(request):
    valor = None

    if request.method == 'POST':
        form = FormPesquisa(request.POST)

        if form.is_valid():
            valor = request.POST['valor']

    elif 'valor' in request.GET:
        valor = request.GET['valor']

    if valor is None or valor == 'None':
        form = FormPesquisa()
    else:
        data = {'valor': valor}
        form = FormPesquisa(initial=data)

    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1

    autorizacoes = Autorizacao.objects.filter()

    if valor is not None:
        autorizacoes = autorizacoes.filter(Q(servidor__first_name__icontains=valor) | Q(servidor__last_name__icontains=valor))

    paginator = Paginator(autorizacoes, settings.NR_REGISTROS_PAGINA)

    try:
        autorizacoes_page = paginator.page(page)
    except:
        autorizacoes_page = paginator.page(paginator.num_pages)

    return render(request, 'autorizacao/consulta.html', {'form': form, 'autorizacoes': autorizacoes_page})
@group_required(settings.PERM_GRUPO_SERVIDOR)
def solicitar(request):

    if request.method == 'POST':
        form = FormAutorizacao(request.POST)
        print form.errors

        if form.is_valid():
            autorizacao = Autorizacao()
            autorizacao.cnh = request.POST["cnh"]
            autorizacao.observacao = request.POST["observacao"]
            autorizacao.servidor_id = request.user.id
            autorizacao.save()

            return redirect("/#/")

    else:
        form = FormAutorizacao()

    return render(request, 'autorizacao/autorizacao.html', {"form":form })