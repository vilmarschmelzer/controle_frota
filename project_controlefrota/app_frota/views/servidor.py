
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from app_frota.models.servidor import Servidor
from app_frota.forms import FormCadastraServidor


#@login_required(login_url='/login/')
def cadastra_servidor(request):

    if request.method == 'POST':

        form = FormCadastraServidor(request.POST)

        if form.is_valid():

            servidor = Servidor()
            servidor.first_name = request.POST["nome"]
            servidor.email = request.POST["email"]
            servidor.password = request.POST["senha"]
            servidor.cpf = request.POST["cpf"]
            for gp in request.POST.getlist('grupos'):
                servidor.groups.add(gp)

            servidor.save()

            #Vilmar
            return redirect("/lista_servidores/")

    else:
        form = FormCadastraServidor()

    return render(request, 'servidor/cadastra_servidor.html', {"cadastra_servidor":form })