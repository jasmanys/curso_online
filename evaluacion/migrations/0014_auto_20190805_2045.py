# Generated by Django 2.2 on 2019-08-06 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluacion', '0013_auto_20190805_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opcionenunciado',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='fotos_opciones_enunciado/', verbose_name='Imagen'),
        ),
    ]