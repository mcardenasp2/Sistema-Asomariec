# Generated by Django 3.0.3 on 2020-10-25 22:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compra', '0011_auto_20201022_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecCom',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 25, 17, 17, 24, 554874)),
        ),
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecEli',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 25, 17, 17, 24, 554874)),
        ),
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecMod',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 25, 17, 17, 24, 554874)),
        ),
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecReg',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 25, 17, 17, 24, 554874)),
        ),
    ]
