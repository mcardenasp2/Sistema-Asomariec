# Generated by Django 3.0.3 on 2021-05-03 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insumo', '0006_insumo_insiva'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumo',
            name='insIva',
            field=models.DecimalField(decimal_places=2, default=0.12, max_digits=10),
        ),
    ]
