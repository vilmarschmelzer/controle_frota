#coding: utf-8 

from django import forms
from appfrota.models.servidor import Servidor

class Form_cadastra_servidor(forms.Form):
	
	nome = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'class':'form-control',
			'placeholder':'Informe o nome do servidor...',
			'id':'nome'
		})
	)

	email = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'class':'form-control',
			'placeholder':'Informe o email do servidor...',
			'id':'email'
		})
	)

	senha = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'class':'form-control',
			'placeholder':'Informe a senha do servidor...',
			'id':'senha'
		})
	)

	cpf = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'class':'form-control',
			'placeholder':'Informe a cpf do servidor...',
			'id':'cpf'
		})
	)