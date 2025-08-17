from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.constancia.models.anio import Anio


class Establecimiento(models.Model):
    progsub = models.CharField(_('PROGSUB'), max_length=5)
    codest = models.CharField(_('CODEST'), max_length=9)
    desest = models.CharField(_('DESEST'), max_length=250)
    anio = models.ForeignKey(Anio, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Establecimiento')
        verbose_name_plural = _('Establecimientos')
        ordering = ['desest']
        unique_together = (("progsub", "codest", "anio"),)

    def __str__(self):
        return '%s - %s : %s' % (str(self.progsub), str(self.codest), self.desest)
