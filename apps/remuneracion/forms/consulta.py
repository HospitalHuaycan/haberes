from django import forms
from django.forms import CharField


class ConsultaForm(forms.Form):
    dni = CharField(label='DNI del Trabajador', required=True, max_length=8, min_length=8)
