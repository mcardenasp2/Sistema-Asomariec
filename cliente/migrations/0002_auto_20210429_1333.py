# Generated by Django 3.0.3 on 2021-04-29 18:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='cliFecMod',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='cliFecReg',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='usuaEli',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='usuaMod',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='usuaReg',
        ),
        migrations.AddField(
            model_name='cliente',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cliente_cliente_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cliente',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cliente_cliente_updated', to=settings.AUTH_USER_MODEL),
        ),
    ]
