from django.db import models
from django.utils.translation import gettext_lazy as _


class Anio(models.Model):
    anio = models.PositiveIntegerField(_('Año'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Año')
        verbose_name_plural = _('Años')
        ordering = ['-anio']

    def __str__(self):
        return str(self.anio)
