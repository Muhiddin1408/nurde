# Generated by Django 5.1.6 on 2025-04-22 20:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0014_specialist_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('education', 'Education'), ('advanced', 'Advanced')], max_length=50)),
                ('name', models.CharField(max_length=255)),
                ('education', models.CharField(max_length=255)),
                ('finish', models.IntegerField()),
                ('specialist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.specialist')),
            ],
        ),
    ]
