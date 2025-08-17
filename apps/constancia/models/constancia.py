from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.constancia.models.anio import Anio
from apps.establecimiento.models.establecimiento import Establecimiento
from apps.trabajador.models.trabajador import Trabajador


class Constancia(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    anio = models.ForeignKey(Anio, on_delete=models.CASCADE)
    codcar = models.CharField(_('CODCAR'), max_length=50, null=True, blank=True)
    codest = models.CharField(_('CODEST'), max_length=50, null=True, blank=True)
    plaza = models.CharField(_('PLAZA'), max_length=6, null=True, blank=True)
    nivel = models.CharField(_('NIVEL'), max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Constancia')
        verbose_name_plural = _('Constacia')
        ordering = ['trabajador__nombre_completo']
        unique_together = (("trabajador", "plaza", "anio"),)

    def __str__(self):
        return '%s - %s' % (self.trabajador.dni, self.trabajador.nombres)

    def establecimiento(self):

        try:
            establecimiento = Establecimiento.objects.get(codest="sdsd")
        except Establecimiento.DoesNotExist:
            establecimiento = ""
        return ""

    def cargo(self):
        return ""

    def nv(self):
        return ""
