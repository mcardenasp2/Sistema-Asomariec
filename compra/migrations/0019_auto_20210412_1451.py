# Generated by Django 3.0.3 on 2021-04-12 19:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compra', '0018_auto_20210408_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecCom',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 12, 14, 51, 36, 266807)),
        ),
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecEli',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 12, 14, 51, 36, 267787)),
        ),
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecMod',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 12, 14, 51, 36, 267787)),
        ),
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecReg',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 12, 14, 51, 36, 267787)),
        ),
    ]
