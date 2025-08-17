from django.contrib import admin

from apps.establecimiento.models.establecimiento import Establecimiento


class EstablecimientoAdmin(admin.ModelAdmin):
    # list_filter = ('tipo',)
    search_fields = ('codest',)


admin.site.register(Establecimiento, EstablecimientoAdmin)
