# Generated by Django 3.0.3 on 2021-04-29 18:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compra', '0008_auto_20210429_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecEli',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 29, 13, 8, 38, 734618)),
        ),
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecMod',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 29, 13, 8, 38, 733642)),
        ),
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecReg',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 29, 13, 8, 38, 733642)),
        ),
    ]
