# Generated by Django 5.1.6 on 2025-04-29 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0018_specialist_city_specialist_gen_specialist_pinfl_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialist',
            name='password',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
