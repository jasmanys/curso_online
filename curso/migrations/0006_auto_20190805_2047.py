# Generated by Django 2.2 on 2019-08-06 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0005_auto_20190803_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiantesubmodulo',
            name='submodulos',
            field=models.ManyToManyField(to='curso.SubModulo', verbose_name='SubModulos cursados'),
        ),
    ]