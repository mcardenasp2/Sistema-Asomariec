# Generated by Django 3.0.3 on 2021-02-18 23:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0011_auto_20210218_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='venFechaFin',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 2, 18, 18, 2, 52, 287094), null=True),
        ),
        migrations.AlterField(
            model_name='venta',
            name='venFechaInici',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 18, 18, 2, 52, 287094)),
        ),
    ]
