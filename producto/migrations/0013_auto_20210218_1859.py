# Generated by Django 3.0.3 on 2021-02-18 23:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0012_auto_20210218_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produccion',
            name='prodcFecElab',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 18, 18, 59, 16, 413436)),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecEli',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 2, 18, 18, 59, 16, 412459), null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecMod',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 2, 18, 18, 59, 16, 412459), null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecReg',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 2, 18, 18, 59, 16, 412459), null=True),
        ),
    ]