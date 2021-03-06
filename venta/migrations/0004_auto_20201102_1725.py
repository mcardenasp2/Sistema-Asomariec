# Generated by Django 3.0.3 on 2020-11-02 22:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0003_auto_20201025_1717'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gastadc',
            options={'ordering': ['id'], 'verbose_name': 'Detalle de Venta', 'verbose_name_plural': 'Detalle de Ventas'},
        ),
        migrations.AlterModelOptions(
            name='venta',
            options={'ordering': ['id'], 'verbose_name': 'Venta', 'verbose_name_plural': 'Ventas'},
        ),
        migrations.AlterField(
            model_name='venta',
            name='venFechaFin',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 2, 17, 25, 53, 376218), null=True),
        ),
        migrations.AlterField(
            model_name='venta',
            name='venFechaInici',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 2, 17, 25, 53, 376218)),
        ),
    ]
