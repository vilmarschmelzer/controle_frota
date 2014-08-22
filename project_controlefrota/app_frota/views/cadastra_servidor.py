
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from app_frota.models.servidor import Servidor

@login_required(login_url='/login/')
def cadastra_servidor(request):
	
	if request.method == 'POST':

		form = Form_cadastra_servidor(request.POST)

		if form.is_valid():
						
			servidor = Servidor()
			servidor.nome = request.POST["nome"]
			servidor.email = request.POST["email"]
			servidor.senha = request.POST["senha"]
			servidor.cpf = request.POST["cpf"]
			servidor.save()

			#Vilmar
			return redirect("/lista_servidores/")


	else:

		form = Form_filmes()
	
	return render(request, 'cadastra_servidor.html', {
		"cadastra_servidor":form
	})