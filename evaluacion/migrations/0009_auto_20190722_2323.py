# Generated by Django 2.2 on 2019-07-23 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluacion', '0008_auto_20190722_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enunciadoevaluacion',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='fotos_enunciado/', verbose_name='Imagen para el enunciado (Opcional)'),
        ),
    ]
