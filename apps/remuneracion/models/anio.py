# if os.path.splitext(os.path.basename(sys.argv[0]))[0] == 'pydoc-script':
# django.setup()


from django.db import models


class Anio(models.Model):
    anio = models.CharField('Año', max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Año'
        verbose_name_plural = 'Años'
        # ordering = ['number']

    def __str__(self):
        return self.anio
