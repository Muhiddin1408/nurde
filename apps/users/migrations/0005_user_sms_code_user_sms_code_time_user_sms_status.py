# Generated by Django 5.1.6 on 2025-04-16 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_address_options_alter_patient_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sms_code',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='sms_code_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='sms_status',
            field=models.BooleanField(default=False),
        ),
    ]
