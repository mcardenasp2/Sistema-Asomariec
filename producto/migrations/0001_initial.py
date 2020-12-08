# Generated by Django 3.0.3 on 2020-12-03 20:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('insumo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prodDescripcion', models.CharField(max_length=100, verbose_name='Descripcion')),
                ('prodFecElab', models.DateTimeField(default=datetime.datetime(2020, 12, 3, 15, 24, 12, 190875))),
                ('prodImagen', models.ImageField(blank=True, null=True, upload_to='producto')),
                ('prodImagen2', models.ImageField(blank=True, null=True, upload_to='producto2')),
                ('prodCantidad', models.IntegerField(default=1)),
                ('prodPrecio', models.DecimalField(decimal_places=2, default=1.25, max_digits=9)),
                ('prodTotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('prodIva', models.DecimalField(decimal_places=2, default=0.12, max_digits=10)),
                ('prodCaracteristica', models.TextField(max_length=400, null=True)),
                ('prodEstprod', models.IntegerField(default=0)),
                ('prodTipo', models.IntegerField(default=1)),
                ('prodEstado', models.BooleanField(default=True, verbose_name='Estado')),
                ('usuaReg', models.IntegerField(blank=True, null=True)),
                ('usuaMod', models.IntegerField(blank=True, null=True)),
                ('usuaEli', models.IntegerField(blank=True, null=True)),
                ('prodFecReg', models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 3, 15, 24, 12, 190875), null=True)),
                ('prodFecMod', models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 3, 15, 24, 12, 190875), null=True)),
                ('prodFecEli', models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 3, 15, 24, 12, 190875), null=True)),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='GastosAdicionales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gastdescripcion', models.CharField(max_length=100)),
                ('gastprecio', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='producto.Producto')),
            ],
            options={
                'verbose_name': 'Detalle Gastos Adicional',
                'verbose_name_plural': 'Detalle Gastos Adicionales',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DetProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detprecio', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('detCantidad', models.IntegerField(default=1)),
                ('detSubtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('insumo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='insumo.Insumo')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='producto.Producto')),
            ],
            options={
                'verbose_name': 'Detalle de Producto',
                'verbose_name_plural': 'Detalle de Productos',
                'ordering': ['id'],
            },
        ),
    ]
