# Generated by Django 3.0.3 on 2021-05-06 23:59

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('catDescripcion', models.CharField(max_length=100, verbose_name='CategoriaDescripcion')),
                ('catEstado', models.BooleanField(default=True, verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
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
            ],
            options={
                'verbose_name': 'Detalle de Producto',
                'verbose_name_plural': 'Detalle de Productos',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='GastosAdicionales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gastdescripcion', models.CharField(max_length=100)),
                ('gastprecio', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
            ],
            options={
                'verbose_name': 'Detalle Gastos Adicional',
                'verbose_name_plural': 'Detalle Gastos Adicionales',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Produccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('prodcFecElab', models.DateTimeField(default=datetime.datetime(2021, 5, 6, 18, 59, 35, 952452))),
                ('prodcCantidad', models.IntegerField(default=1)),
                ('prodcTotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('prodcEstado', models.BooleanField(default=True, verbose_name='Estado')),
                ('prodcTipo', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name': 'Produccion',
                'verbose_name_plural': 'Producciones',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('prodDescripcion', models.CharField(max_length=100, verbose_name='Descripcion')),
                ('prodImagen', models.ImageField(blank=True, null=True, upload_to='producto')),
                ('prodImagen2', models.ImageField(blank=True, null=True, upload_to='producto2')),
                ('prodCantidad', models.IntegerField(blank=True, default=0, null=True)),
                ('prodPrecio', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('prodTotal', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('prodIva', models.DecimalField(decimal_places=2, default=0.12, max_digits=10)),
                ('prodCaracteristica', models.TextField(blank=True, max_length=400, null=True)),
                ('prodEstprod', models.IntegerField(blank=True, default=1)),
                ('prodTipo', models.IntegerField(blank=True, default=2)),
                ('prodEstado', models.BooleanField(default=True, verbose_name='Estado')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='producto.Categoria')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ['id'],
            },
        ),
    ]
