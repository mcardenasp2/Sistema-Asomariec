# Generated by Django 3.0.3 on 2020-10-12 21:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compra', '0003_auto_20201012_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecCom',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 12, 16, 17, 33, 237420)),
        ),
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecEli',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 12, 16, 17, 33, 237420)),
        ),
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecMod',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 12, 16, 17, 33, 237420)),
        ),
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecReg',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 12, 16, 17, 33, 237420)),
        ),
    ]
