# Generated by Django 3.0.3 on 2021-04-29 21:34

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('producto', '0021_auto_20210429_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='produccion',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='produccion',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
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
        migrations.AlterField(
            model_name='produccion',
            name='prodcFecElab',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 29, 16, 34, 36, 626849)),
        ),
    ]
