#coding:utf-8
from django.shortcuts import render, redirect
from app_frota.models import Veiculo
from app_frota.forms import FormVeiculo
from app_frota.forms.pesquisa import FormPesquisa
from decorators.permissoes import group_required
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import logout


@group_required(settings.PERM_GRUPO_ADM)
def adicionar(request):

    if request.method == 'POST':

        form = FormVeiculo(request.POST)

        if form.is_valid():

            if str(settings.PERM_GRUPO_ADM) in request.POST.getlist('grupos') \
                    and not request.user.is_superuser:
                return render(request, 'veiculo/adiciona_veiculo.html',
                              {	'form': form, 'msg_erro': 'Usuário logado não é "Super usuário", '
                                                             'não será possui cadastrar servidor com permissão "Administrador"'})

            if settings.PERM_GRUPO_ADM in request.POST.getlist('grupos'):
                veiculo = Veiculo()

            else:
                veiculo = Veiculo()

            veiculo.nome = request.POST["nome"]
            veiculo.marca_id = request.POST["marca"]
            veiculo.modelo = request.POST["modelo"]
            veiculo.chassis = request.POST["chassis"]
            veiculo.placa = request.POST["placa"]

            veiculo.save()

            return redirect("/consultar-veiculos/")

    else:
        form = FormVeiculo()

    return render(request, 'veiculo/adicionar_veiculo.html', {"form":form })


@group_required(settings.PERM_GRUPO_ADM)
def editar(request, veiculo_id):

    request.session['id_veiculo'] = veiculo_id

    veiculo = Veiculo.objects.get(pk=veiculo_id)

    if request.method == 'POST':

        form = FormVeiculo(request.POST)

        if form.is_valid():

            if str(settings.PERM_GRUPO_ADM) in request.POST.getlist('grupos') \
                    and not request.user.is_superuser:
                return render(request, 'veiculo/adiciona_veiculo.html',
                              {	'form': form, 'msg_erro': 'Usuário logado não é "Super usuário", '
                                                             'não será possui cadastrar servidor com permissão "Administrador"'})

            veiculo.nome = request.POST["nome"]
            veiculo.marca_id = request.POST["marca"]
            veiculo.modelo = request.POST["modelo"]
            veiculo.chassis = request.POST["chassis"]
            veiculo.placa = request.POST["placa"]

            veiculo.save()

            return redirect("/consultar-veiculos/")

    else:

        dados_veiculo = {
            'nome':veiculo.nome,
            'marca':veiculo.marca_id,
            'modelo':veiculo.modelo,
            'chassis':veiculo.chassis,
            'placa':veiculo.placa
        }

        form = FormVeiculo(initial=dados_veiculo)

    return render(request, 'veiculo/editar_veiculo.html', {"form":form, "id":veiculo_id})


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

    veiculos = Veiculo.objects.filter(~Q(id=valor))

    paginator = Paginator(veiculos, settings.NR_REGISTROS_PAGINA)

    try:
        veiculos_page = paginator.page(page)
    except:
        veiculos_page = paginator.page(paginator.num_pages)

    return render(request, 'veiculo/consulta.html', {'form': form, 'veiculos': veiculos_page})