# Generated by Django 3.0.3 on 2021-01-24 03:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0006_auto_20210123_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='venFechaFin',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 1, 23, 22, 46, 45, 538384), null=True),
        ),
        migrations.AlterField(
            model_name='venta',
            name='venFechaInici',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 23, 22, 46, 45, 538384)),
        ),
    ]
