# Generated by Django 3.0.3 on 2020-10-12 20:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compra', '0002_auto_20201012_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecCom',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 12, 15, 10, 44, 367208)),
        ),
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecEli',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 12, 15, 10, 44, 367208)),
        ),
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecMod',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 12, 15, 10, 44, 367208)),
        ),
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecReg',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 12, 15, 10, 44, 367208)),
        ),
    ]
