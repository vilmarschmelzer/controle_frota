#coding:utf-8
from django.shortcuts import render, redirect, HttpResponse
from app_frota.models import Emprestimo, Rota, Autorizacao, Veiculo, Servidor
from decorators.permissoes import group_required
from django.conf import settings
from app_frota.forms.pesquisa import FormPesquisa
from app_frota.forms.emprestimo import FormSolicitar, FormVisualizar
from django.db.models import Q
from django.core.paginator import Paginator
from django.db import transaction
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.utils import simplejson


@group_required(settings.PERM_GRUPO_SERVIDOR)
@transaction.commit_on_success
def solicitar(request):

    solcitar_condutor = Servidor().is_conduzir(request.user.id)

    ''' select a.id as id from app_frota_veiculo a inner join app_frota_emprestimo b on (a.id=b.veiculo_id)
    where not b.dt_saida between "2016-02-21 07:50:00" and "2016-02-21 08:49:00" '''

    if request.method == 'POST':

        form = FormSolicitar(request.POST['estado_origem'], request.POST['estado_destino'], solcitar_condutor, request.POST)

        if form.is_valid():
            form.get_data_saida()

            rota = Rota()
            rota.cidade_origem_id = request.POST['cidade_origem']
            rota.endereco_origem = request.POST['endereco_origem']
            rota.cidade_destino_id = request.POST['cidade_destino']
            rota.endereco_destino = request.POST['endereco_destino']
            rota.save()

            emprestimo = Emprestimo()
            emprestimo.rota = rota
            emprestimo.dt_saida = form.get_data_saida()
            emprestimo.dt_devolucao = form.get_data_devolucao()
            emprestimo.observacao = request.POST['observacao']

            if 'veiculo' in request.POST:
                emprestimo.veiculo_id = request.POST['veiculo']

            if 'solicitar_condutor' not in request.POST:
                emprestimo.condutor_id = request.user.id
            emprestimo.servidor_id = request.user.id

            emprestimo.save()

            return redirect('/')
    else:
        form = FormSolicitar(None, None, solcitar_condutor)

    return render(request, 'emprestimo/solicita.html', {'form': form, 'solcitar_condutor': solcitar_condutor})


@group_required(settings.PERM_GRUPO_ADM)
@transaction.commit_on_success
def visualizar(request, id):

    if request.method == 'POST':
        form = FormVisualizar(id, request.POST)

        if form.is_valid():
            form.save()

            return redirect('/consultar-emprestimos/')

    else:
        form = FormVisualizar(id)

    return render(request, 'emprestimo/visualizar.html', {'form': form})

@group_required(settings.PERM_GRUPO_SERVIDOR)
@transaction.commit_on_success
def visualizar_emprestimo_serv(request, id):

    emprestimo = Emprestimo.objects.get(id = id)
    if request.method == 'POST':
        form = FormSolicitar(request.POST['estado_origem'], request.POST['estado_destino'], False, request.POST)

        if form.is_valid():

            rota = emprestimo.rota
            rota.cidade_origem_id = request.POST['cidade_origem']
            rota.endereco_origem = request.POST['endereco_origem']
            rota.cidade_destino_id = request.POST['cidade_destino']
            rota.endereco_destino = request.POST['endereco_destino']
            rota.save()

            emprestimo.rota = rota
            emprestimo.dt_saida = form.get_data_saida()
            emprestimo.dt_devolucao = form.get_data_devolucao()
            emprestimo.observacao = request.POST['observacao']

            form.save()

            return redirect('/consultar-emprestimos_serv/')

    else:

        data = {'dt_saida':emprestimo.dt_saida,
                'dt_devolucao':emprestimo.dt_devolucao,
                'observacao':emprestimo.observacao,
                'origem':emprestimo.rota.endereco_origem,
                'destino':emprestimo.rota.endereco_destino,
                }
        form = FormSolicitar(emprestimo.rota.cidade_origem.estado_id, emprestimo.rota.cidade_destino.estado_id, False, initial=data)

    return render(request, 'emprestimo/solicita.html', {'form': form,})

@group_required(settings.PERM_GRUPO_ADM)
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

    emprestimos = Emprestimo.objects.filter()

    if valor is not None:
        emprestimos = emprestimos.filter(Q(servidor__first_name__icontains=valor) | Q(servidor__last_name__icontains=valor))

    paginator = Paginator(emprestimos, settings.NR_REGISTROS_PAGINA)

    try:
        emprestimos_page = paginator.page(page)
    except:
        emprestimos_page = paginator.page(paginator.num_pages)

    return render(request, 'emprestimo/consulta_emprestimo.html', {'form': form, 'emprestimos': emprestimos_page})

@group_required(settings.PERM_GRUPO_SERVIDOR)
def consulta_emp_serv(request):

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

    emprestimos = Emprestimo.objects.filter(servidor_id = request.user.id)

    if valor is not None:
        emprestimos = emprestimos.filter(Q(dt_saida=valor) | Q(dt_devolucao=valor))

    paginator = Paginator(emprestimos, settings.NR_REGISTROS_PAGINA)

    try:
        emprestimos_page = paginator.page(page)
    except:
        emprestimos_page = paginator.page(paginator.num_pages)

    return render(request, 'emprestimo/consulta_emprestimo_serv.html', {'form': form, 'emprestimos': emprestimos_page})

@csrf_exempt
def veiculos_disponiveis(request):

    form = FormSolicitar(None, None, None, request.POST)

    form.is_valid()
    if 'dt_saida' not in form.errors and 'dt_devolucao' not in form.errors and 'hora_devolucao' not in form.errors:

        veiculos = Veiculo().get_veiculos_disponiveis(form.get_data_saida(),form.get_data_devolucao())
        json = serializers.serialize('json', veiculos)

    else:

        msg = ''
        if 'dt_saida' in form.errors:
            msg += u'Data saída : '+form.errors['dt_saida'].as_text()+'<br>'
        if 'dt_devolucao' in form.errors:
            msg += u'Data devolucao: '+form.errors['dt_devolucao'].as_text()+'<br>'
        if 'hora_devolucao' in form.errors:
            msg += u'Hora devolucão: '+form.errors['hora_devolucao'].as_text()+'<br>'
        json = simplejson.dumps({'success': False, 'msg': msg}, ensure_ascii=False)

    return HttpResponse(json, mimetype='application/json')
