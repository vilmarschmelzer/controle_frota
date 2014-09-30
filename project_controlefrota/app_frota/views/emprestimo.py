#coding:utf-8
from django.shortcuts import render, redirect, HttpResponse
from app_frota.models import Emprestimo, Rota, Autorizacao, Veiculo
from decorators.permissoes import group_required
from django.conf import settings
from app_frota.forms.pesquisa import FormPesquisa
from app_frota.forms.emprestimo import FormSolicitar
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

    ''' select a.id as id from app_frota_veiculo a inner join app_frota_emprestimo b on (a.id=b.veiculo_id)
    where not b.dt_saida between "2016-02-21 07:50:00" and "2016-02-21 08:49:00" '''

    if request.method == 'POST':

        form = FormSolicitar(request.POST['estado_origem'], request.POST['estado_destino'], request.POST)

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
        form = FormSolicitar(None, None)

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


@csrf_exempt
def veiculos_disponiveis(request):

    form = FormSolicitar(None,None,request.POST)
    msg = ''

    form.is_valid()
    if 'dt_saida' not in form.errors and 'dt_devolucao' not in form.errors and 'hora_devolucao' not in form.errors:

        veiculos = Veiculo.objects.raw('select id from app_frota_veiculo where id not in (select a.id as id from app_frota_veiculo a inner join app_frota_emprestimo b on (a.id=b.veiculo_id) '
                            +'where not b.dt_saida between \'%s\' and \'%s\')' % (form.get_data_saida(),form.get_data_devolucao()))

        json = serializers.serialize('json', veiculos)

        #json = simplejson.dumps({'success': True, 'veiculos': data_json}, ensure_ascii=False)

    else:

        msg = ''
        if 'dt_saida' in form.errors:
            msg += u'Data saída : '+form.errors['dt_saida'].as_text()+'<br>'
        if 'dt_devolucao' in form.errors:
            msg += u'Data devolucao: '+form.errors['dt_devolucao'].as_text()+'<br>'
        if 'hora_devolucao' in form.errors:
            msg += u'Hora devolucão: '+form.errors['hora_devolucao'].as_text()+'<br>'
        json = simplejson.dumps({'success': False, 'msg': msg}, ensure_ascii=False)

    print form.get_data_saida()
    print form.get_data_devolucao()

    return HttpResponse(json, mimetype='application/json')
