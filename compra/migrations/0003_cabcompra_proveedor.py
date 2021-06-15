# Generated by Django 3.0.3 on 2021-06-15 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('compra', '0002_detcompra_insumo'),
        ('proveedor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cabcompra',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='proveedor.Proveedor'),
        ),
    ]
