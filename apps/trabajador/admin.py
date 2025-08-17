from django.contrib import admin

from apps.trabajador.models.trabajador import Trabajador


class TrabajadorAdmin(admin.ModelAdmin):
    # list_filter = ('depedencia__nombre',)
    search_fields = ('dni',)


admin.site.register(Trabajador, TrabajadorAdmin)
