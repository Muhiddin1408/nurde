# Generated by Django 5.1.6 on 2025-04-18 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_sms_code_user_sms_code_time_user_sms_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='passport',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='pin',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
