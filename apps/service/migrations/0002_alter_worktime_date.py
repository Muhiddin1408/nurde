# Generated by Django 5.1.6 on 2025-04-18 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worktime',
            name='date',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
