# Generated by Django 5.1.6 on 2025-02-12 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0002_infoclinic_description_photos_service'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Photos',
            new_name='Photo',
        ),
    ]
