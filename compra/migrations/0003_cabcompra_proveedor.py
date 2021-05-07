# Generated by Django 3.0.3 on 2021-05-06 23:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('proveedor', '0001_initial'),
        ('compra', '0002_detcompra_insumo'),
    ]

    operations = [
        migrations.AddField(
            model_name='cabcompra',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='proveedor.Proveedor'),
        ),
    ]
