#coding: utf-8

from django import forms
from app_frota.models import Marca
from django.db.models import Q

class FormVeiculo(forms.Form):

    nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Informe o nome do veiculo...',
            'id':'nome'
        })
    )

    marca = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class':'form-control',
            'id':'Marca'
        }),
        queryset=Marca.objects.all(),
        empty_label="Selecione uma marca"
    )

    chassis = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Informe o chassis do veiculo...',
            'id':'chassis'
        })
    )

    modelo = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Informe o modelo do veiculo...',
            'id':'modelo'
        })
    )

    placa = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Informe a placa do veiculo...',
            'id':'placa'
        })
    )

    ativo = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class':'form-control',
            'id':'ativo'
        })
    )