# Generated by Django 5.1.6 on 2025-04-27 19:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0017_comment_created_at'),
        ('utils', '0006_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='symptomsubtype',
            name='category',
        ),
        migrations.AddField(
            model_name='symptomtype',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='utils.category'),
        ),
    ]
