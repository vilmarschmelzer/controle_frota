#coding:utf-8
from django.shortcuts import render, redirect
from app_frota.models import Emprestimo, Rota
from decorators.permissoes import group_required
from django.conf import settings
from app_frota.forms.pesquisa import FormPesquisa
from app_frota.forms.emprestimo import FormSolicitar
from django.db.models import Q
from django.core.paginator import Paginator
from django.db import transaction
from datetime import datetime


@group_required(settings.PERM_GRUPO_SERVIDOR)
@transaction.commit_on_success
def solicitar(request):

    print request.POST

    if request.method == 'POST':
        print request.POST
        form = FormSolicitar(request.POST['estado_origem'], request.POST['estado_destino'], request.POST)

        if form.is_valid():

            dt_saida = datetime.strptime('%i/%i/%i %s:00' % (int(request.POST['dt_saida_day']),
                                                             int(request.POST['dt_saida_month']),
                                                             int(request.POST['dt_saida_year']),
                                                             request.POST['hora_saida']), '%d/%m/%Y %H:%M:00')

            dt_devolucao = datetime.strptime('%i/%i/%i %s:00' % (int(request.POST['dt_devolucao_day']),
                                                             int(request.POST['dt_devolucao_month']),
                                                             int(request.POST['dt_devolucao_year']),
                                                             request.POST['hora_devolucao']), '%d/%m/%Y %H:%M:00')

            rota = Rota()
            rota.cidade_origem_id = request.POST['cidade_origem']
            rota.endereco_origem = request.POST['endereco_origem']
            rota.cidade_destino_id = request.POST['cidade_destino']
            rota.endereco_destino = request.POST['endereco_destino']
            rota.save()

            emprestimo = Emprestimo()
            emprestimo.rota = rota
            emprestimo.dt_saida = dt_saida
            emprestimo.dt_devolucao = dt_devolucao
            emprestimo.observacao = request.POST['observacao']

            if 'solicitar_condutor' not in request.POST:
                emprestimo.condutor_id = request.user.id
            emprestimo.servidor_id = request.user.id
            #veiculo = models.ForeignKey(Veiculo, null=True)

            emprestimo.save()

            return redirect('/')
    else:
        form = FormSolicitar(None,None)

    return render(request, 'emprestimo/solicita.html', {'form': form })


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
