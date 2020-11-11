# Generated by Django 3.0.3 on 2020-11-04 02:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0011_auto_20201102_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='prodFecElab',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 3, 21, 20, 8, 812685)),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecEli',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 3, 21, 20, 8, 812685), null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecMod',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 3, 21, 20, 8, 812685), null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecReg',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 3, 21, 20, 8, 812685), null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodPrecio',
            field=models.DecimalField(decimal_places=2, default=1.25, max_digits=9),
        ),
    ]
