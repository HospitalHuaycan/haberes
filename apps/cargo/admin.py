from django.contrib import admin

from apps.cargo.models.cargo import Cargo


class CargoAdmin(admin.ModelAdmin):
    # list_filter = ('tipo',)
    search_fields = ('codcar',)


admin.site.register(Cargo, CargoAdmin)
