# Generated by Django 3.0.3 on 2021-04-29 20:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0018_auto_20210429_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produccion',
            name='prodcFecElab',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 29, 15, 49, 5, 213904)),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecEli',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 29, 15, 49, 5, 211952), null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecMod',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 29, 15, 49, 5, 211952), null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecReg',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 29, 15, 49, 5, 211952), null=True),
        ),
    ]
