# Generated by Django 3.0.3 on 2020-11-04 02:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0006_auto_20201102_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='venFechaFin',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 3, 21, 20, 8, 816675), null=True),
        ),
        migrations.AlterField(
            model_name='venta',
            name='venFechaInici',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 3, 21, 20, 8, 816675)),
        ),
    ]
