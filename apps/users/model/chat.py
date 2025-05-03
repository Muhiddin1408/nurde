from django.db import models

from apps.basic.models import Specialist
from apps.users.model import Patient
from apps.users.models import User


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True, related_name='children')


class Message(models.Model):
    STATUS = (
        ('user', 'user'),
        ('admin', 'admin'),
    )
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True, blank=True, related_name='messages')
    status = models.CharField(max_length=100, choices=STATUS, default='user')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='admin')
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='messages', blank=True, null=True)


class ChatDoctor(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(Specialist, on_delete=models.CASCADE, null=True, blank=True, related_name='chat_sp')


class MessageDoctor(models.Model):
    STATUS = (
        ('user', 'user'),
        ('admin', 'admin'),
    )
    room = models.ForeignKey(ChatDoctor, on_delete=models.CASCADE, null=True, blank=True, related_name='doctormessages')
    status = models.CharField(max_length=100, choices=STATUS, default='user')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='admin_doctor')
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='messages', blank=True, null=True)
