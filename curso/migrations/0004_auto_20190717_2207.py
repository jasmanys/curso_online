# Generated by Django 2.2 on 2019-07-18 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0003_auto_20190717_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submodulo',
            name='numero',
            field=models.IntegerField(default=1, verbose_name='Número SubMódulo'),
        ),
    ]