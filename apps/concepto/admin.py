from django.contrib import admin

from apps.concepto.models.concepto import Concepto


class ConceptoAdmin(admin.ModelAdmin):
    # list_filter = ('tipo',)
    search_fields = ('codcon',)


admin.site.register(Concepto, ConceptoAdmin)
