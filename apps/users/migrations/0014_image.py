# Generated by Django 5.1.6 on 2025-04-23 04:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0013_remove_clinic_image'),
        ('users', '0013_patient_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('status', models.BooleanField(default=False)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.clinic')),
            ],
        ),
    ]
