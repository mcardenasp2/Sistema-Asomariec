# Generated by Django 3.0.3 on 2021-04-29 20:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('insumo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='insumo',
            name='insFecMod',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='insFecReg',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='usuaEli',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='usuaMod',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='usuaReg',
        ),
        migrations.AddField(
            model_name='insumo',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='insumo',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='insumo',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='insumo_insumo_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='insumo',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='insumo_insumo_updated', to=settings.AUTH_USER_MODEL),
        ),
    ]
