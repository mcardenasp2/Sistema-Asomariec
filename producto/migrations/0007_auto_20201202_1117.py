# Generated by Django 3.0.3 on 2020-12-02 16:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0006_auto_20201124_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='prodFecElab',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 2, 11, 17, 11, 64390)),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecEli',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 2, 11, 17, 11, 64390), null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecMod',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 2, 11, 17, 11, 64390), null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecReg',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 2, 11, 17, 11, 64390), null=True),
        ),
    ]
