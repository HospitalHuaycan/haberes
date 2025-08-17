from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.constancia.models.anio import Anio
from apps.constancia.models.constancia import Constancia
from apps.trabajador.models.trabajador import Trabajador

MESES = (
    (1, 'ENERO'),
    (2, 'FEBRERO'),
    (3, 'MARZO'),
    (4, 'ABRIL'),
    (5, 'MAYO'),
    (6, 'JUNIO'),
    (7, 'JULIO'),
    (8, 'AGOSTO'),
    (9, 'SEPTIEMBRE'),
    (10, 'OCTUBRE'),
    (11, 'NOVIEMBRE'),
    (12, 'DICIEMBRE'),
)


class ConstanciaDetalle(models.Model):
    constancia = models.ForeignKey(Constancia, on_delete=models.CASCADE, null=True, blank=True)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    anio = models.ForeignKey(Anio, on_delete=models.CASCADE)
    mes = models.PositiveIntegerField(_('MES'), choices=MESES, default=1)
    codeje = models.CharField(_('CODEJE'), max_length=50, null=True, blank=True)
    codfun = models.CharField(_('CODFUN'), max_length=50, null=True, blank=True)
    codpro = models.CharField(_('CODPRO'), max_length=50, null=True, blank=True)
    codsud = models.CharField(_('CODSUB'), max_length=50, null=True, blank=True)
    tipopla = models.CharField(_('TIPOPLA'), max_length=50, null=True, blank=True)
    progsub = models.CharField(_('PROGSUB'), max_length=50, null=True, blank=True)
    codest = models.CharField(_('CODEST'), max_length=50, null=True, blank=True)
    codcom = models.CharField(_('CODCOM'), max_length=50, null=True, blank=True)
    serv = models.CharField(_('SERV'), max_length=50, null=True, blank=True)
    codcar = models.CharField(_('CODCAR'), max_length=50, null=True, blank=True)
    codniv = models.CharField(_('CODNIV'), max_length=50, null=True, blank=True)
    concepto = models.CharField(_('Concepto'), max_length=4)
    monto = models.DecimalField(_('Monto'), max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Contancia Detalle')
        verbose_name_plural = _('Contancias Detalle')
        ordering = ['mes', 'concepto']

    def __str__(self):
        return '%s -  [ %s - %s ] - %s - %s' % (
            self.trabajador.dni, self.anio.anio, self.get_mes_display(), self.concepto, str(self.monto))
