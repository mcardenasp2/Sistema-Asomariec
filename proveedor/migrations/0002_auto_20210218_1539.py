# Generated by Django 3.0.3 on 2021-02-18 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proveedor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='proTelefono',
            field=models.CharField(blank=True, max_length=25, verbose_name='Telefono'),
        ),
    ]
