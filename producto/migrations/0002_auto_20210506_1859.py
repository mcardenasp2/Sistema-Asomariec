# Generated by Django 3.0.3 on 2021-05-06 23:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('insumo', '0002_auto_20210506_1859'),
        ('producto', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='producto_producto_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='producto',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='producto_producto_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='produccion',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='producto.Producto'),
        ),
        migrations.AddField(
            model_name='produccion',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='producto_produccion_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='produccion',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='producto_produccion_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='gastosadicionales',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='producto.Producto'),
        ),
        migrations.AddField(
            model_name='detproducto',
            name='insumo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='insumo.Insumo'),
        ),
        migrations.AddField(
            model_name='detproducto',
            name='produccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='producto.Produccion'),
        ),
        migrations.AddField(
            model_name='categoria',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='producto_categoria_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='categoria',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='producto_categoria_updated', to=settings.AUTH_USER_MODEL),
        ),
    ]
