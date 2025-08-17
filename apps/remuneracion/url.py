from django.urls import path

from apps.remuneracion.views.main import consulta_quinta_categoria
from apps.remuneracion.views.report_pdf_remuneracion import print_simulator

app_name = 'remuneracion'

urlpatterns = [
    path('', consulta_quinta_categoria, name='index'),
    path('report', print_simulator, name='report'),
]
