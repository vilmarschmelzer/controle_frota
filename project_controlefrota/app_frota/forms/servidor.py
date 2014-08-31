#coding: utf-8

from django import forms
from django.contrib.auth.models import Group, User
from django.db.models import Q


class FormCadastraServidor(forms.Form):

    nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Informe o nome do servidor...',
            'id':'nome'
        })
    )

    email = forms.EmailField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Informe o email do servidor...',
            'id':'email'
        })
    )

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


class FormSalvarPerfil(FormCadastraServidor):

    nova_senha = forms.CharField(widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'Informe nova senha',
            'id':'nova_senha'
        }),required=False)
    confirmar_senha = forms.CharField(widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'Confirmar senha',
            'id':'confirmar_senha'
        }),required=False)

    def __init__(self, id, *args, **kwargs):
        super(FormSalvarPerfil, self).__init__(*args, **kwargs)
        self.fields.pop('grupos')
        self.fields.pop('cpf')
        self.id = id

    def clean_usuario(self):
        usuario = self.cleaned_data['usuario']

        existe = User.objects.filter(Q(username=usuario), ~Q(id=self.id))

        if len(existe) > 0:
            raise forms.ValidationError('Usuário já cadastrado')

        return usuario

    def clean_senha(self):
        senha = self.cleaned_data['senha']

        if self.id > 0:
            user = User.objects.filter(id=self.id, username=self.cleaned_data['email']).get()
            if user.check_password(self.cleaned_data['senha']) is False:
                raise forms.ValidationError('Senha invalida!')

        return senha

    def clean_confirmar_senha(self):
        if 'nova_senha' not in self.cleaned_data and self.cleaned_data['confirmar_senha'] != self.cleaned_data['senha']:
            raise forms.ValidationError('Confirmação da senha não confere!')

        if 'nova_senha' in self.cleaned_data and self.cleaned_data['confirmar_senha'] != self.cleaned_data['nova_senha']:
            raise forms.ValidationError('Confirmação da senha não confere!')

        return self.cleaned_data['confirmar_senha']