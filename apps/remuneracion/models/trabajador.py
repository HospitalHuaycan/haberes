import os
import sys

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.remuneracion.models.dependencia import Dependencia

if os.path.splitext(os.path.basename(sys.argv[0]))[0] == 'pydoc-script':
    import django

    django.setup()

TIPOS_TRABAJADOR = (
    (1, 'NOMB. PROFESIONAL'),
    (2, 'NOMB. ADMINISTR.'),
)


class Trabajador(models.Model):
    dni = models.CharField(_('DNI'), max_length=8, unique=True)
    apellidos_nombres = models.CharField(_('Apellidos y nombres'), max_length=130)
    fecha_nacimiento = models.DateField(_('Fecha de nacimiento'))
    depedencia = models.ForeignKey(Dependencia, on_delete=models.CASCADE)
    plaza = models.CharField(_('Plaza'), max_length=10, unique=True)
    cargo = models.CharField(_('Cargo'), max_length=100)
    tipo = models.PositiveIntegerField(choices=TIPOS_TRABAJADOR, default=1)
    nombres = models.CharField(_('Nombres'), max_length=130, null=True, blank=True)
    apellido_paterno = models.CharField(_('Apellido paterno'), max_length=130, null=True, blank=True)
    apellido_materno = models.CharField(_('Apellido materno'), max_length=130, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Trabajador')
        verbose_name_plural = _('Trabajadores')
        # ordering = ['number']

    def __str__(self):
        return "%s - %s [%s] " % (self.dni, self.apellidos_nombres, self.depedencia.nombre)
