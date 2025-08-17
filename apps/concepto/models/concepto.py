from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.constancia.models.anio import Anio


class Concepto(models.Model):
    tiparch = models.PositiveIntegerField(_('TIPARCH'))
    codcon = models.CharField(_('CODCON'), max_length=4)
    descon = models.CharField(_('DESCON'), max_length=100)
    abrcon = models.CharField(_('ABRCON'), max_length=50)
    modifi = models.CharField(_('MODIFI'), max_length=2, null=True, blank=True)
    descon1 = models.CharField(_('DESCON1'), max_length=50, null=True, blank=True)
    mes = models.PositiveIntegerField(_('MES'))
    anio = models.ForeignKey(Anio, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Concepto')
        verbose_name_plural = _('Conceptos')
        ordering = ['codcon', 'mes', 'anio']
        unique_together = (("tiparch", "codcon", "mes", "anio"),)

    def __str__(self):
        return '%s - %s - %s : %s / %s' % (
            str(self.tiparch), str(self.codcon), self.abrcon, str(self.mes), str(self.anio))
