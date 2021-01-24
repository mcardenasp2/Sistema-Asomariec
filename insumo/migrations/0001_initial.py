# Generated by Django 3.0.3 on 2021-01-23 22:11

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
                ('catDescripcion', models.CharField(max_length=50, verbose_name='Descripcion')),
                ('catEstado', models.BooleanField(default=True, verbose_name='Estado')),
                ('usuaReg', models.IntegerField(blank=True, null=True)),
                ('usuaMod', models.IntegerField(blank=True, null=True)),
                ('usuaEli', models.IntegerField(blank=True, null=True)),
                ('catFecReg', models.DateTimeField(auto_now_add=True, null=True)),
                ('catFecMod', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='UnidadMedidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medDescripcion', models.CharField(max_length=50, verbose_name='Medidad')),
                ('medEstado', models.BooleanField(default=True, verbose_name='Estado')),
                ('usuaReg', models.IntegerField(blank=True, null=True)),
                ('usuaMod', models.IntegerField(blank=True, null=True)),
                ('usuaEli', models.IntegerField(blank=True, null=True)),
                ('medFecReg', models.DateTimeField(auto_now_add=True, null=True)),
                ('medFecMod', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Medida',
                'verbose_name_plural': 'Medidas',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Insumo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insCod', models.CharField(max_length=100)),
                ('insDescripcion', models.CharField(max_length=50, verbose_name='Descripcion')),
                ('insModelo', models.CharField(max_length=50, verbose_name='Modelo')),
                ('insPrecio', models.DecimalField(decimal_places=2, default=1.25, max_digits=10)),
                ('insImagen', models.ImageField(blank=True, null=True, upload_to='fotos/%Y/%m/%d')),
                ('insStock', models.IntegerField(blank=True, default=0, null=True, verbose_name='Stock')),
                ('insEstado', models.BooleanField(default=True, verbose_name='Estado')),
                ('usuaReg', models.IntegerField(blank=True, null=True)),
                ('usuaMod', models.IntegerField(blank=True, null=True)),
                ('usuaEli', models.IntegerField(blank=True, null=True)),
                ('insFecReg', models.DateTimeField(auto_now_add=True, null=True)),
                ('insFecMod', models.DateTimeField(auto_now=True, null=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='insumo.Categoria')),
                ('medida', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='insumo.UnidadMedidad')),
            ],
            options={
                'verbose_name': 'Insumo',
                'verbose_name_plural': 'Insumos',
                'ordering': ['id'],
            },
        ),
    ]
