# Generated by Django 3.0.3 on 2020-10-21 00:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0005_auto_20201016_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='prodFecElab',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 20, 19, 58, 50, 168723)),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecEli',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 10, 20, 19, 58, 50, 168723), null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecMod',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 10, 20, 19, 58, 50, 168723), null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecReg',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 10, 20, 19, 58, 50, 168723), null=True),
        ),
    ]
