# Generated by Django 5.1.6 on 2025-04-26 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_remove_address_city_remove_address_home_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='no',
            new_name='number',
        ),
        migrations.AlterField(
            model_name='address',
            name='entrance',
            field=models.CharField(blank=True, max_length=125, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='floor',
            field=models.CharField(blank=True, max_length=125, null=True),
        ),
    ]
