# Generated by Django 3.0.3 on 2021-04-29 19:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compra', '0012_auto_20210429_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecEli',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 29, 14, 22, 57, 67711)),
        ),
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecMod',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 29, 14, 22, 57, 67711)),
        ),
        migrations.AlterField(
            model_name='cabcompra',
            name='ccoFecReg',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 29, 14, 22, 57, 67711)),
        ),
    ]