from django.db import models
from django.utils.translation import gettext_lazy as _


class TipoPlanilla(models.Model):
    t_pla = models.PositiveIntegerField(_('T_PLA'), unique=True)
    des_pla = models.CharField(_('DES_PLA'), max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Tipo planilla')
        verbose_name_plural = _('Tipos de planillas')
        ordering = ['t_pla']

    def __str__(self):
        return '%s - %s' % (self.t_pla, self.des_pla)
