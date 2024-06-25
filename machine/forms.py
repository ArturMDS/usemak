from django import forms
from django.forms import ModelForm
from .models import Estabelecimento, Atualizacao


class FormHomepage(forms.Form):
    email = forms.EmailField(label=False)


class CreateAtualizacaoForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(CreateAtualizacaoForm, self).__init__(*args, **kwargs)
        self.fields['estabelecimento'].queryset = Estabelecimento.objects.filter(usuario=user)

    class Meta:
        model = Atualizacao
        fields = ['nome', 'arquivo', 'estabelecimento']

