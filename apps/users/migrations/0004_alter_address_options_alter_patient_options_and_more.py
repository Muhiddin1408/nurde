# Generated by Django 5.1.6 on 2025-03-10 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_c_lat_patient_latitude_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name': 'Адреса', 'verbose_name_plural': 'Адреса'},
        ),
        migrations.AlterModelOptions(
            name='patient',
            options={'verbose_name': 'Пациенты', 'verbose_name_plural': 'Пациенты'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователи', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
