# Generated by Django 5.1.6 on 2025-04-27 18:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_order_price_alter_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosis', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('comment', models.TextField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
        ),
        migrations.CreateModel(
            name='Recommendations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommendation', models.TextField()),
                ('diagnosis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.diagnosis')),
            ],
        ),
    ]
