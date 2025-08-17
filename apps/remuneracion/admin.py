from django.contrib import admin

from apps.remuneracion.models.anio import Anio
from apps.remuneracion.models.dependencia import Dependencia
from apps.remuneracion.models.detalle_remuneracion import DetalleRemuneracion
from apps.remuneracion.models.entidad_ejecutora import EntidadEjecutora
from apps.remuneracion.models.remuneracion import Remuneracion
from apps.remuneracion.models.trabajador import Trabajador


class RemuneracionesAdmin(admin.ModelAdmin):
    # list_filter = ('depedencia__nombre',)
    search_fields = ('trabajador__plaza', 'trabajador__dni')


admin.site.register(Anio)
admin.site.register(Remuneracion, RemuneracionesAdmin)
admin.site.register(DetalleRemuneracion, RemuneracionesAdmin)
admin.site.register(Trabajador)
admin.site.register(EntidadEjecutora)
admin.site.register(Dependencia)
