# Generated by Django 3.0.3 on 2020-10-11 00:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prvDescripcion', models.CharField(max_length=50, verbose_name='Descripcion')),
                ('prvEstado', models.BooleanField(default=True, verbose_name='Estado')),
                ('usuaReg', models.IntegerField(blank=True, null=True)),
                ('usuaMod', models.IntegerField(blank=True, null=True)),
                ('usuaEli', models.IntegerField(blank=True, null=True)),
                ('prvFecReg', models.DateTimeField(auto_now_add=True, null=True)),
                ('prvFecMod', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Provincia',
                'verbose_name_plural': 'Provincias',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proEmpresa', models.CharField(max_length=80, verbose_name='Empresa')),
                ('proRuc', models.CharField(max_length=13, verbose_name='Ruc')),
                ('proDireccion', models.CharField(max_length=80, verbose_name='Direccion')),
                ('proTelefono', models.CharField(max_length=25, verbose_name='Telefono')),
                ('proEmail', models.EmailField(max_length=80, verbose_name='Email')),
                ('proEstado', models.BooleanField(default=True, verbose_name='Estado')),
                ('usuaReg', models.IntegerField(blank=True, null=True)),
                ('usuaMod', models.IntegerField(blank=True, null=True)),
                ('usuaEli', models.IntegerField(blank=True, null=True)),
                ('proFecReg', models.DateTimeField(auto_now_add=True, null=True)),
                ('proFecMod', models.DateTimeField(auto_now=True, null=True)),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='proveedor.Provincia')),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
                'ordering': ['id'],
            },
        ),
    ]
