# Generated by Django 5.1.6 on 2025-04-29 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_chatroom_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birth_day',
            field=models.DateField(blank=True, null=True),
        ),
    ]
