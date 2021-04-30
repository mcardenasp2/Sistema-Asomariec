# Generated by Django 3.0.3 on 2021-04-29 17:38

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('producto', '0007_auto_20210427_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='categoria',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='categoria',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='categoria',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='produccion',
            name='prodcFecElab',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 29, 12, 38, 25, 8241)),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecEli',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 29, 12, 38, 25, 7265), null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecMod',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 29, 12, 38, 25, 7265), null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodFecReg',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 29, 12, 38, 25, 7265), null=True),
        ),
    ]
