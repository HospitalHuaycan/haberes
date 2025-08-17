from django.contrib import admin

from apps.constancia.models.anio import Anio
from apps.constancia.models.constancia import Constancia
from apps.constancia.models.constancia_detalle import ConstanciaDetalle


class ConstanciaDetalleAdmin(admin.ModelAdmin):
    # list_filter = ('tipo',)
    search_fields = ('trabajador__dni',)


admin.site.register(Anio)
admin.site.register(Constancia, ConstanciaDetalleAdmin)
admin.site.register(ConstanciaDetalle, ConstanciaDetalleAdmin)
