from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.constancia.models.anio import Anio


class Cargo(models.Model):
    codant = models.CharField(_('CODANT'), max_length=4, null=True, blank=True)
    codcar = models.CharField(_('CODCAR'), max_length=4)
    descar = models.CharField(_('DESCAR'), max_length=250)
    anio = models.ForeignKey(Anio, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Cargo')
        verbose_name_plural = _('Cargos')
        ordering = ['codcar']
        unique_together = ('codcar', 'anio',)

    def __str__(self):
        return '%s - %s - %s' % (self.codant if self.codant else " ", self.codcar, self.descar)
