# Generated by Django 3.0.3 on 2021-04-12 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=100)),
                ('nombre', models.CharField(max_length=100)),
                ('icono', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=100)),
                ('activo', models.BooleanField(default=True)),
                ('orden', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Módulo',
                'verbose_name_plural': 'Módulos',
                'ordering': ['orden'],
            },
        ),
        migrations.CreateModel(
            name='ModuloGrupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(blank=True, max_length=200)),
                ('prioridad', models.IntegerField(blank=True, null=True)),
                ('grupos', models.ManyToManyField(to='auth.Group')),
                ('modulos', models.ManyToManyField(to='seguridad.Modulo')),
            ],
            options={
                'verbose_name': 'Grupo de Módulos',
                'verbose_name_plural': 'Grupos de Módulos',
                'ordering': ('prioridad', 'nombre'),
            },
        ),
    ]