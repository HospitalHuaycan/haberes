from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.constancia.views.constancia import ConstanciaList, GenerarConstanciaView
from apps.constancia.views.constancia_reporte_pdf import print_constancia_pdf
from apps.constancia.views.constancia_reporte_excel import print_constancia_excel

app_name = 'constancia'

urlpatterns = [
    path('list', login_required(ConstanciaList.as_view()), name='list'),
    path('generar', login_required(GenerarConstanciaView.as_view()), name='generar'),
    path('pdf', print_constancia_pdf, name='pdf'),
    path('excel', print_constancia_excel, name='excel'),

]
