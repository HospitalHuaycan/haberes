# from captcha.fields import CaptchaField
from django import forms
from django.forms import CharField


class ConsultaForm(forms.Form):
    dni = CharField(label='DNI del Trabajador', required=True, max_length=8)
    # captcha = CaptchaField(label='CAPTCHA', required=True)
