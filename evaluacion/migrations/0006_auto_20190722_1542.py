# Generated by Django 2.2 on 2019-07-22 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evaluacion', '0005_auto_20190722_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enunciadoevaluacion',
            name='submodulo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curso.SubModulo', unique=True, verbose_name='SubModulo'),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='modulo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curso.Modulo', unique=True, verbose_name='Módulo'),
        ),
    ]