# Generated by Django 5.1.6 on 2025-04-18 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_weekday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='pinfl',
            field=models.CharField(blank=True, max_length=125, null=True),
        ),
    ]
