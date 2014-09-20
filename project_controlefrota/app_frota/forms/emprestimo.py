#coding: utf-8
from django import forms
from app_frota.models import Estado, Cidade
from django.forms.extras.widgets import SelectDateWidget


class FormSolicitar(forms.Form):

    def __init__(self, estado_origem_id, estado_destino_id, *args, **kwargs):
        super(FormSolicitar, self).__init__(*args, **kwargs)

        self.fields['dt_saida'] = forms.DateField(
            widget=SelectDateWidget(attrs={
                'id': 'dt_saida'
            })
        )

        self.fields['hora_saida'] = forms.TimeField(
            widget=forms.TimeInput(format='%H:%M', attrs={
                'class': 'form-control',
                'id': 'dt_saida'
            })
        )

        self.fields['dt_devolucao'] = forms.DateField(
            widget=SelectDateWidget(attrs={
                'id': 'dt_devolucao'
            })
        )

        self.fields['hora_devolucao'] = forms.TimeField(
            widget=forms.TimeInput(format='%H:%M', attrs={
                'class': 'form-control',
                'id': 'hora_devolucao'
            })
        )

        self.fields['observacao'] = forms.CharField(required=False, widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'senha'}))

        self.fields['solicitar_condutor'] = forms.BooleanField(required=False,
            widget=forms.CheckboxInput(attrs={
                'class': 'form-control',
                'id': 'solicitar_condutor'
            })
        )

        if estado_origem_id == '':
            estado_origem_id = None

        if estado_destino_id == '':
            estado_destino_id = None

        self.fields['estado_origem'] = forms.ModelChoiceField(widget=forms.Select(attrs={'id': 'estado_origem',
                                                                                  'class': 'form-control'}),
                                                       queryset=Estado.objects.all(),
                                                       empty_label="Selecione um Estado")

        self.fields['cidade_origem'] = forms.ModelChoiceField(widget=forms.Select(attrs={'id': 'cidade_origem',
                                                                                  'class': 'form-control'}),
                                                       queryset=Cidade.objects.filter(estado_id=estado_origem_id).all(),
                                                       empty_label="Selecione uma Cidade")

        self.fields['estado_destino'] = forms.ModelChoiceField(widget=forms.Select(attrs={'id': 'estado_destino',
                                                                                  'class': 'form-control'}),
                                                       queryset=Estado.objects.all(),
                                                       empty_label="Selecione um Estado")

        self.fields['cidade_destino'] = forms.ModelChoiceField(widget=forms.Select(attrs={'id': 'cidade_destino',
                                                                                  'class': 'form-control'}),
                                                       queryset=Cidade.objects.filter(estado_id=estado_destino_id).all(),
                                                       empty_label="Selecione uma Cidade")

        self.fields['endereco_origem'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'endereco_origem'
            })
        )

        self.fields['endereco_destino'] = forms.CharField(
            max_length=200,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'endereco_destino'
            })
        )
