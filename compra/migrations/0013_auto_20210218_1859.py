# Generated by Django 3.0.3 on 2021-02-18 23:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compra', '0012_auto_20210218_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecCom',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 18, 18, 59, 16, 410507)),
        ),
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecEli',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 18, 18, 59, 16, 410507)),
        ),
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecMod',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 18, 18, 59, 16, 410507)),
        ),
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecReg',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 18, 18, 59, 16, 410507)),
        ),
    ]