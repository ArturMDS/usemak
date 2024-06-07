from django import forms
from .models import Usuario


class FormHomepage(forms.Form):
    email = forms.EmailField(label=False)

