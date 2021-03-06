# Generated by Django 3.0.3 on 2020-10-11 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliNombre', models.CharField(blank=True, max_length=150, verbose_name='Nombre')),
                ('cliApellido', models.CharField(blank=True, max_length=150, verbose_name='Apellido')),
                ('cliRuc', models.CharField(max_length=13, unique=True, verbose_name='Ruc')),
                ('cliTelefono', models.CharField(blank=True, max_length=13, verbose_name='Telefono')),
                ('cliDireccion', models.CharField(blank=True, max_length=100, verbose_name='Direccion')),
                ('cliGenero', models.CharField(choices=[('male', 'Masculino'), ('female', 'Femenino')], default='male', max_length=10, verbose_name='Sexo')),
                ('cliEmail', models.EmailField(blank=True, max_length=50, verbose_name='Email')),
                ('cliEstado', models.BooleanField(default=True, verbose_name='Estado')),
                ('usuaReg', models.IntegerField(blank=True, null=True)),
                ('cliFecReg', models.DateTimeField(auto_now_add=True, null=True)),
                ('usuaMod', models.IntegerField(blank=True, null=True)),
                ('cliFecMod', models.DateTimeField(auto_now=True, null=True)),
                ('usuaEli', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['id'],
            },
        ),
    ]
