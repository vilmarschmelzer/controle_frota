#coding:utf-8
from django.shortcuts import render, redirect
from app_frota.models import Servidor, Administrador
from app_frota.forms import FormCadastraServidor, FormSalvarPerfil
from decorators.permissoes import group_required
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from app_frota.forms.pesquisa import FormPesquisa
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import logout


@group_required(settings.PERM_GRUPO_ADM)
def adicionar(request):

    if request.method == 'POST':

        form = FormCadastraServidor(request.POST)

        if form.is_valid():

            if str(settings.PERM_GRUPO_ADM) in request.POST.getlist('grupos') \
                    and not request.user.is_superuser:
                return render(request, 'servidor/adicionar.html',
                              {	'form': form, 'msg_erro': 'Usuário logado não é "Super usuário", '
                                                             'não será possui cadastrar servidor com permissão "Administrador"'})

            if settings.PERM_GRUPO_ADM in request.POST.getlist('grupos'):
                servidor = Administrador()
            else:
                servidor = Servidor()

            servidor.first_name = request.POST["nome"]
            servidor.email = request.POST["email"]
            servidor.username = request.POST["email"]
            servidor.set_password(request.POST["senha"])
            servidor.cpf = request.POST["cpf"]

            servidor.save()

            for gp in request.POST.getlist('grupos'):

                User(servidor.id).groups.add(gp)

            #Vilmar
            return redirect("/lista_servidores/")

    else:
        form = FormCadastraServidor()

    return render(request, 'servidor/adicionar.html', {"form":form })


@group_required(settings.PERM_GRUPO_ADM)
def editar(request, user_id):

    user = User.objects.get(pk=user_id)
    grupos_user = user.groups.values_list('id').all()
    msg_erro = None
    if request.method == 'POST':
        grupos_selecionado = request.POST.getlist('grupo')

        if str(settings.PERM_GRUPO_ADM) in request.POST.getlist('grupo') and not request.user.is_superuser:
            msg_erro = 'Usuário logado não é "Super usuário", não será possui adicionar o "Administrador" ao usuário.'
        else:
            for grupo in grupos_selecionado:
                if (int(grupo),) not in grupos_user:
                    user.groups.add(grupo)

            for grupo in user.groups.all():
                print 'group : ',grupo
                if str(grupo.id) not in grupos_selecionado:
                    user.groups.remove(grupo)

            if 'ativo' in request.POST:
                user.is_active = True
            else:
                user.is_active = False

            user.save()
            return redirect('/consultar-servidores/')

    grupos = Group.objects.all()

    for gp in grupos:
        if (gp.id,) in grupos_user:
            gp.checked = 'checked'
        else:
            gp.checked = ''

    if user.is_active:
        user.checked = 'checked'
    else:
        user.checked = ''

    return render(request, 'servidor/editar.html', {'servidor': user, 'grupos': grupos, 'msg_erro': msg_erro})


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

    users = User.objects.filter(~Q(id=request.user.id))

    if not request.user.is_superuser:
        users = users.filter(Q(is_superuser=False), ~Q(groups__in=[settings.PERM_GRUPO_ADM]))

    if valor is not None:
        users = users.filter(Q(first_name__icontains=valor) | Q(last_name__icontains=valor))

    paginator = Paginator(users, settings.NR_REGISTROS_PAGINA)

    try:
        users_page = paginator.page(page)
    except:
        users_page = paginator.page(paginator.num_pages)

    return render(request, 'servidor/consulta.html', {'form': form, 'servidores': users_page})


@login_required
def salvar_perfil(request):

    if request.method == 'POST':
        form = FormSalvarPerfil(request.user.id, request.POST)

        if form.is_valid():
            user = User.objects.get(pk=request.user.id)
            if request.POST['nova_senha'] != '':
                user.set_password(request.POST['confirmar_senha'])

            user.first_name = request.POST['nome']
            user.email = request.POST['email']

            user.save()

            logout(request)
            return redirect('/')
    else:
        data = {'nome': request.user.first_name, 'email': request.user.email, '': request.user.username}
        form = FormSalvarPerfil(request.user.id, initial=data)

    return render(request, 'servidor/perfil.html', {	'form': form})
