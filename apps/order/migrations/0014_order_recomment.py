# Generated by Django 5.0.14 on 2025-05-26 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_recommendations_order_recommendations_result_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='recomment',
            field=models.BooleanField(default=False),
        ),
    ]
