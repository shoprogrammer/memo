# Generated by Django 5.1.3 on 2024-11-24 00:51

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memo', '0007_alter_memomodel_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='memomodel',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
