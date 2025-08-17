import os
import sys

from apps.remuneracion.models.trabajador import Trabajador

if os.path.splitext(os.path.basename(sys.argv[0]))[0] == 'pydoc-script':
    import django

    django.setup()

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.remuneracion.models.anio import Anio
from apps.remuneracion.models.remuneracion import Remuneracion

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


class DetalleRemuneracion(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    anio = models.ForeignKey(Anio, on_delete=models.CASCADE)
    remuneracion = models.ForeignKey(Remuneracion, on_delete=models.CASCADE, null=True, blank=True)
    mes = models.PositiveIntegerField(_('MES'), choices=MESES, default=1)
    ingresos_remu_v_p = models.DecimalField(_('REMU/V.P.'), max_digits=10, decimal_places=2)
    ingresos_otras_ue = models.DecimalField(_('OTRAS UE'), max_digits=10, decimal_places=2)
    ingresos_otros = models.DecimalField(_('OTROS'), max_digits=10, decimal_places=2)
    ingresos_total = models.DecimalField(_('TOTAL'), max_digits=10, decimal_places=2)
    retencion_efectuar = models.DecimalField(_('RETENCION X EFECTUAR'), max_digits=10, decimal_places=2)
    retencion_remu_v_p = models.DecimalField(_('REMU/V.P.'), max_digits=10, decimal_places=2)
    retencion_adicional = models.DecimalField(_('ADICIONAL'), max_digits=10, decimal_places=2)
    retencion_otros = models.DecimalField(_('OTROS'), max_digits=10, decimal_places=2)
    retencion_total = models.DecimalField(_('TOTAL'), max_digits=10, decimal_places=2)
    total_pagar = models.DecimalField(_('TOTAL A PAGAR O DEVOLVER'), max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Detalle Remuneracion')
        verbose_name_plural = _('Detalles Remuneracione')
        ordering = ['mes']

    def __str__(self):
        return '%s - %s - %s (%s)' % (
            self.trabajador.plaza, self.trabajador.apellidos_nombres, self.get_mes_display(), str(self.retencion_total))
