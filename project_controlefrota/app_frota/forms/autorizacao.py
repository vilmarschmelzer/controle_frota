#coding: utf-8

from django import forms

class FormAutorizacao(forms.Form):

    cnh = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Informe o numero da cnh...',
            'id':'cnh'
        })
    )

    observacao = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Informe o porque requer a autorização...',
            'id':'obervacao'
        })
    )