# Generated by Django 2.2 on 2019-07-24 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluacion', '0009_auto_20190722_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enunciadoevaluacion',
            name='tipo_respuesta',
            field=models.IntegerField(choices=[(0, 'Respuesta única'), (1, 'Opción múltiple')], verbose_name='Tipo de Respuesta'),
        ),
        migrations.AlterField(
            model_name='opcionenunciado',
            name='opcion',
            field=models.TextField(max_length=200, verbose_name='Enunciado'),
        ),
    ]