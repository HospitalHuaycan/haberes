from django import forms
from django.utils.translation import gettext_lazy as _

from apps.constancia.models.anio import Anio
from apps.constancia.models.constancia import Constancia
from apps.util.generic_filters import forms as gf


class ConstanciaForm(forms.ModelForm):
    class Meta:
        model = Constancia
        fields = '__all__'


def convert_object_to_filter(list):
    choice_new = ()
    for i in list:
        choice_new += ((str(i.id), str(i.anio)),)
    return choice_new


class ConstanciaListFilter(gf.FilteredForm):
    anio_list = Anio.objects.all()

    # anio = gf.ChoiceField(label=_('Año'), choices=convert_object_to_filter(anio_list))

    def get_order_by_choices(self):
        return [('anio', '1')]
