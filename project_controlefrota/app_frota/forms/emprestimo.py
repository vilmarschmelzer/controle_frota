#coding: utf-8
from django import forms
from app_frota.models import Estado, Cidade, Veiculo
from django.forms.extras.widgets import SelectDateWidget
from django.forms.util import ErrorList
from datetime import datetime


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

        self.fields['estado_origem'] = forms.ModelChoiceField(
            widget=forms.Select(attrs={'id': 'estado_origem', 'class': 'form-control'}),
            queryset=Estado.objects.all(),
            empty_label="Selecione um Estado")

        self.fields['cidade_origem'] = forms.ModelChoiceField(
            widget=forms.Select(attrs={'id': 'cidade_origem', 'class': 'form-control'}),
            queryset=Cidade.objects.filter(estado_id=estado_origem_id).all(),
            empty_label="Selecione uma Cidade")

        self.fields['estado_destino'] = forms.ModelChoiceField(
            widget=forms.Select(attrs={'id': 'estado_destino', 'class': 'form-control'}),
            queryset=Estado.objects.all(),
            empty_label="Selecione um Estado")

        self.fields['cidade_destino'] = forms.ModelChoiceField(
            widget=forms.Select(attrs={'id': 'cidade_destino', 'class': 'form-control'}),
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
            widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'endereco_destino'})
        )

        '''self.fields['veiculo'] = forms.ModelChoiceField(
            required=False,
            widget=forms.Select(attrs={'id': 'veiculo', 'class': 'form-control'}),
            queryset=Veiculo().get_veiculos_disponiveis(None, None),
            empty_label="Selecione uma Cidade")
        '''
    def get_data_saida(self):
        cleaned_data = self.cleaned_data
        try:
            return datetime.strptime('%s %s' % (cleaned_data['dt_saida'], cleaned_data['hora_saida']),'%Y-%m-%d %H:%M:00')
        except:
            return None

    def get_data_devolucao(self):
        cleaned_data = self.cleaned_data
        try:
            return datetime.strptime('%s %s' % (cleaned_data['dt_devolucao'], cleaned_data['hora_devolucao']), '%Y-%m-%d %H:%M:00')
        except:

            return None

    def clean(self):
        cleaned_data = self.cleaned_data

        try:
            if self.get_data_saida() < datetime.now():
                self._errors['dt_saida'] = ErrorList(['Data menor que atual'])

            elif self.get_data_saida() >= self.get_data_devolucao():
                self._errors['dt_devolucao'] = ErrorList(['Data de devolução inválida'])
                self._errors['hora_devolucao'] = ErrorList(['Hora de devolução inválida'])
        except:
            pass

        return cleaned_data