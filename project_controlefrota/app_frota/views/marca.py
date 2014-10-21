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
				nome=request.POST['marca']
				)
			get_marca.save()
			return HttpResponseRedirect('/')
    else:
        form = FormMarca()

    return render(request, 'marca/cadastrar_marca.html', {'form': form})