# Generated by Django 3.0.3 on 2021-01-24 03:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0003_auto_20210123_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produccion',
            name='prodcFecElab',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 23, 22, 13, 27, 237993)),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecElab',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 23, 22, 13, 27, 237018)),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecEli',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 1, 23, 22, 13, 27, 237018), null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecMod',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 1, 23, 22, 13, 27, 237018), null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecReg',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 1, 23, 22, 13, 27, 237018), null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodTotal',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, null=True),
        ),
    ]
