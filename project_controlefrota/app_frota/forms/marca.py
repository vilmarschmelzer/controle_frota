#coding utf-8
from django import forms

class FormMarca(forms.Form):
    marca = forms.CharField(label='Marca', max_length=100)