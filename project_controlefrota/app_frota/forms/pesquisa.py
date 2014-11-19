#coding: utf-8
from django import forms


class FormPesquisa(forms.Form):
    valor = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'id':'pesquisa_valor'}))