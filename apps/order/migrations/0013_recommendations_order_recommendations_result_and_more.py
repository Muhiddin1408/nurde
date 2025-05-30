# Generated by Django 5.1.6 on 2025-05-15 18:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0018_remove_symptomsubtype_category_symptomtype_category'),
        ('order', '0012_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendations',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.order'),
        ),
        migrations.AddField(
            model_name='recommendations',
            name='result',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='recommendations',
            name='diagnosis',
        ),
        migrations.AddField(
            model_name='recommendations',
            name='diagnosis',
            field=models.ManyToManyField(blank=True, null=True, to='clinic.symptom'),
        ),
    ]
