# Generated by Django 3.0.3 on 2021-04-29 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('insumo', '0003_auto_20210429_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unidadmedidad',
            name='medFecMod',
        ),
        migrations.RemoveField(
            model_name='unidadmedidad',
            name='medFecReg',
        ),
        migrations.RemoveField(
            model_name='unidadmedidad',
            name='usuaEli',
        ),
        migrations.RemoveField(
            model_name='unidadmedidad',
            name='usuaMod',
        ),
        migrations.RemoveField(
            model_name='unidadmedidad',
            name='usuaReg',
        ),
    ]