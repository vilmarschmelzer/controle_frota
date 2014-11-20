#coding:utf-8
from django.shortcuts import render, redirect, HttpResponse
from app_frota.models import Veiculo
from app_frota.forms import FormVeiculo
from app_frota.forms.pesquisa import FormPesquisa
from decorators.permissoes import group_required
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
from latex import LatexDocument
from django.template.loader import render_to_string


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
            veiculo.ativo = form.cleaned_data["ativo"]

            veiculo.save()

            return redirect("/consultar-veiculos/")

    else:

        dados_veiculo = {
            'nome':veiculo.nome,
            'marca':veiculo.marca_id,
            'modelo':veiculo.modelo,
            'chassis':veiculo.chassis,
            'placa':veiculo.placa,
            'ativo':veiculo.ativo
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

    if valor:

        id = 0

        try:
            id = int(valor)
        except:
            pass

        veiculos = Veiculo.objects.filter(Q(id=id)|Q(nome__icontains=valor)|Q(marca__nome__icontains=valor)|Q(modelo__icontains=valor)|Q(placa__icontains=valor))
    else:
        veiculos = Veiculo.objects.all()


    paginator = Paginator(veiculos, settings.NR_REGISTROS_PAGINA)

    try:
        veiculos_page = paginator.page(page)
    except:
        veiculos_page = paginator.page(paginator.num_pages)

    return render(request, 'veiculo/consulta.html', {'form': form, 'veiculos': veiculos_page})


def _valor(request):
    valor = None

    if request.method == 'POST':
        form = FormPesquisa(request.POST)

        if form.is_valid():
            valor = request.POST['valor']

    elif 'valor' in request.GET:
        valor = request.GET['valor']

    return valor


def _form(valor):
    if valor is None or valor == 'None':
        form = FormPesquisa()
    else:
        data = {'valor': valor}
        form = FormPesquisa(initial=data)

    return form


def _consulta(valor):

    sql = 'select a.*, (select count(id) from app_frota_emprestimo where veiculo_id=a.id) as count from app_frota_veiculo a '

    parametros = []

    try:
        valor = int(valor)

        sql += 'where a.id = %s '
        parametros.append(valor)
    except:

        if valor:
            valor = '%'+valor+'%'

            sql += 'where UPPER(a.nome) like UPPER(%s) or UPPER(a.modelo) like UPPER(%s) or UPPER(a.placa) like UPPER(%s) '
            parametros.append(valor)
            parametros.append(valor)
            parametros.append(valor)
    sql += 'order by a.nome'

    return Veiculo.objects.raw(sql, parametros)


@group_required(settings.PERM_GRUPO_ADM)
def relatorio(request):
    valor = _valor(request)
    form = _form(valor)

    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1

    veiculos = _consulta(valor)

    paginator = Paginator(list(veiculos), settings.NR_REGISTROS_PAGINA)

    try:
        veiculos_page = paginator.page(page)
    except:
        veiculos_page = paginator.page(paginator.num_pages)

    return render(request, 'veiculo/relatorio.html', {'form': form, 'veiculos': veiculos_page})


@group_required(settings.PERM_GRUPO_ADM)
def imprimir_relatorio(request):
    valor = _valor(request)

    veiculos = _consulta(valor)


    veiculos = list(veiculos)

    latex = render_to_string('veiculo/imprimir_relatorio.tex', {'veiculos': veiculos})

    #Transdorma em documento latex
    tex = LatexDocument(latex.encode('utf-8'))

    #Transforma em pedf
    pdf = tex.as_pdf()

    response = HttpResponse(pdf, mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s.pdf' % 'relatorio'

    # abre o pdf na propria aba
    # return HttpResponse(response, mimetype='application/pdf')
    # baixar o arquivo direto
    return response
