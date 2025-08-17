from django.db import models
from django.utils.translation import gettext_lazy as _


class EntidadEjecutora(models.Model):
    codigo = models.CharField(_('Código'), max_length=30, unique=True)
    nombre = models.CharField(_('Nombre'), max_length=850)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Entidad Ejecutora')
        verbose_name_plural = _('Entidades Ejecutoras')
        # ordering = ['number']

    def __str__(self):
        return "%s - %s " % (self.codigo, self.nombre)
