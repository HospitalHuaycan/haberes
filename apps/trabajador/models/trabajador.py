from django.db import models
from django.utils.translation import gettext_lazy as _

TIPOS_TRABAJADOR = (
    (1, 'NOMB. PROFESIONAL'),
    (2, 'NOMB. ADMINISTR.'),

)


class Trabajador(models.Model):
    dni = models.CharField(_('DNI'), max_length=8, unique=True)
    nombres = models.CharField(_('Nombres'), max_length=150)
    apellido_paterno = models.CharField(_('Apellido paterno'), max_length=250)
    apellido_materno = models.CharField(_('Apellido materno'), max_length=250)
    fecha_nacimiento = models.DateField(_('Fecha de nacimiento'), null=True, blank=True)
    sexo = models.CharField(_('SEXO'), max_length=1)
    nro_hijos = models.PositiveIntegerField(_('NÚMERO DE HIJOS'), default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    nombre_completo = models.CharField(_('Nombre completo'), max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = _('Trabajador')
        verbose_name_plural = _('Trabajadores')
        # ordering = ['number']

    def save(self, *args, **kwargs):
        self.nombre_completo = self.apellido_paterno + " " + self.apellido_materno + " " + self.nombres
        super(Trabajador, self).save(*args, **kwargs)

    def __str__(self):
        return "%s - %s [%s %s] " % (self.dni, self.nombres, self.apellido_paterno, self.apellido_materno)

    def get_full_name(self):
        return "%s %s %s" % (self.nombres, self.apellido_paterno, self.apellido_materno)

    def get_full_name_two(self):
        return "%s %s %s" % (self.apellido_paterno, self.apellido_materno, self.nombres)
