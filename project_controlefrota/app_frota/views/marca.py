from django.shortcuts import render
from django.http import HttpResponseRedirect
from app_frota.forms.marca import FormMarca
from app_frota.models.marca import Marca
from decorators.permissoes import group_required
from django.conf import settings


@group_required(settings.PERM_GRUPO_ADM)
def cadastrar_marca(request):
    if request.method == 'POST':
        form = FormMarca(request.POST)
        if form.is_valid():
			get_marca = Marca(
				nome=request.POST['marca'], 
				status = True
				)
			get_marca.save()
			return HttpResponseRedirect('/')
    else:
        form = FormMarca()

    return render(request, 'marca/cadastrar_marca.html', {'form': form})

@group_required(settings.PERM_GRUPO_ADM)
def editar_marca(request, id_marca):
	marca_info = Marca.objects.get(id = id_marca)
	if request.method == 'POST':
		marca_info.nome = request.POST['editar_nome_marca']
		marca_info.status = (True if request.POST['editar_status_marca'] == "1" else False)
		marca_info.save()
		return HttpResponseRedirect('/listar-marcas/')
	else:
		return render(request, 'marca/editar_marca.html', {'marca': marca_info})

@group_required(settings.PERM_GRUPO_ADM)
def listar_marcas(request):
	marcas = Marca.objects.all()
	return render(request, 'marca/listar_marcas.html', {'marcas': marcas})
