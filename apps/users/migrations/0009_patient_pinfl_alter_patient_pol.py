# Generated by Django 5.1.6 on 2025-04-18 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_user_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='pinfl',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='pol',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
