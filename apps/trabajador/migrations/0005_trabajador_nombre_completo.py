
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trabajador', '0004_auto_20210513_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='trabajador',
            name='nombre_completo',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Nombre completo'),
        ),
    ]
