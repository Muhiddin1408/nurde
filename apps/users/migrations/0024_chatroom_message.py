# Generated by Django 5.1.6 on 2025-04-28 18:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_ankita_first_name_ankita_last_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='users.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('user', 'user'), ('admin', 'admin')], default='user', max_length=100)),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='messages')),
                ('admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin', to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='users.chatroom')),
            ],
        ),
    ]
