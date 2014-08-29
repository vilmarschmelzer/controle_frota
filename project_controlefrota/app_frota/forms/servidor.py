#coding: utf-8

from django import forms
from django.contrib.auth.models import Group


class FormCadastraServidor(forms.Form):

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

    usuario = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Informe o usuário do servidor...',
        'id':'nome'
        }))

    senha = forms.CharField(widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'Informe a senha do servidor...',
            'id':'senha'}))

    cpf = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Informe a cpf do servidor...',
            'id':'cpf'
        })
    )
    grupos = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={
            'class':'form-control', 'id':'grupos'}))