import os
import sys

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.remuneracion.models.entidad_ejecutora import EntidadEjecutora

if os.path.splitext(os.path.basename(sys.argv[0]))[0] == 'pydoc-script':
    import django

    django.setup()


class Dependencia(models.Model):
    entidad_ejecutora = models.ForeignKey(EntidadEjecutora, on_delete=models.CASCADE)
    codigo = models.CharField(_('Código'), max_length=30, unique=True)
    nombre = models.CharField(_('Nombre'), max_length=850)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Dependencia')
        verbose_name_plural = _('Dependencias')
        # ordering = ['number']

    def __str__(self):
        return "%s - %s [%s] " % (self.codigo, self.nombre, self.entidad_ejecutora.nombre)
