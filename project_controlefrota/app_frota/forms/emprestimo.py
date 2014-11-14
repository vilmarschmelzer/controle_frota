#coding: utf-8
from django import forms
from app_frota.models import Estado, Cidade, Veiculo, Emprestimo, Servidor
from django.forms.util import ErrorList
from datetime import datetime
from django.db.models import Q


class FormSolicitar(forms.Form):

    def __init__(self, estado_origem_id, estado_destino_id, solcitar_condutor, *args, **kwargs):
        super(FormSolicitar, self).__init__(*args, **kwargs)

        self.fields['dt_saida'] = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'],
            widget=forms.DateTimeInput(attrs={
                'class': 'form-control',
                'id': 'dt_saida'
            })
        )

        self.fields['dt_devolucao'] = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'],
            widget=forms.DateTimeInput(attrs={
                'class': 'form-control',
                'id': 'dt_devolucao'
            })
        )

        self.fields['observacao'] = forms.CharField(required=False, widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'senha'}))

        if solcitar_condutor:

            self.fields['solicitar_condutor'] = forms.BooleanField(required=False,
                widget=forms.CheckboxInput(attrs={
                    'class': 'form-control',
                    'id': 'solicitar_condutor'
                })
            )

        else:
            self.fields['solicitar_condutor'] = forms.BooleanField(required=False,
                widget=forms.CheckboxInput(attrs={
                    'class': 'form-control',
                    'id': 'solicitar_condutor',
                    'checked': '',
                    'disabled': ''
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

    def get_data_saida(self):
        cleaned_data = self.cleaned_data

        try:
            return cleaned_data['dt_saida']
        except:
            return None

    def get_data_devolucao(self):
        cleaned_data = self.cleaned_data
        try:
            return cleaned_data['dt_devolucao']
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

from django.utils.safestring import mark_safe
class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


CHOICES = (
    (None, "Verificar"),
    (True, "Sim"),
    (False, "Não"),
)

class FormVisualizar(forms.Form):

    def __init__(self, id, *args, **kwargs):

        self.emprestimo = Emprestimo.objects.get(pk=id)

        data = {'veiculo': self.emprestimo.veiculo.id,
                'condutor': self.emprestimo.condutor,
                'aprovado': self.emprestimo.aprovado}

        super(FormVisualizar, self).__init__(initial=data, *args, **kwargs)


        veiculos = [(x.id, x) for x in Veiculo().get_veiculos_disponiveis(self.emprestimo.dt_saida, self.emprestimo.dt_devolucao, id)]

        veiculos.insert(0, ('', 'Selecione um veiculo'))

        self.fields['veiculo'] = forms.ChoiceField(
            required=False,
            widget=forms.Select(attrs={'id': 'veiculo', 'class': 'form-control'}),
            choices=veiculos)

        self.fields['condutor'] = forms.ModelChoiceField(
            required=False,
            widget=forms.Select(attrs={'id': 'condutor', 'class': 'form-control'}),
            queryset=Servidor.objects.filter(~Q(id=self.emprestimo.servidor_id)),
            empty_label="Selecione um condutor")

        self.fields['aprovado'] = forms.NullBooleanField(widget=forms.RadioSelect(renderer=HorizontalRadioRenderer,
                                                                                  choices=CHOICES))

    def clean_aprovado(self):
        aprovado = self.cleaned_data['aprovado']

        if aprovado:

            veiculo = self.cleaned_data['veiculo']

            if veiculo == '':
                self._errors['veiculo'] = ErrorList(['Selecione um veiculo'])

            condutor = self.cleaned_data['condutor']

            if not self.emprestimo.condutor and condutor is None:
                self._errors['condutor'] = ErrorList(['Selecione um condutor'])

        return aprovado

    def save(self):
        emprestimo = self.emprestimo

        aprovado = self.cleaned_data['aprovado']
        veiculo = self.cleaned_data['veiculo']

        emprestimo.aprovado = aprovado
        emprestimo.veiculo_id = veiculo

        if 'condutor' in self.cleaned_data:
            emprestimo.condutor_id = self.cleaned_data['condutor']

        return emprestimo.save()