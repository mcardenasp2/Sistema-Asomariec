# Generated by Django 3.0.3 on 2020-11-24 21:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0004_auto_20201118_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='venFechaFin',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 24, 16, 20, 49, 219963), null=True),
        ),
        migrations.AlterField(
            model_name='venta',
            name='venFechaInici',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 24, 16, 20, 49, 219963)),
        ),
    ]