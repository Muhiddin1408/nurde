from django.db import models

from apps.users.models import User


class Card(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    card_number = models.IntegerField()
    expire = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class CardInfo(models.Model):
    parent = models.ForeignKey('Card', related_name='children', on_delete=models.CASCADE)
    token = models.TextField()
    card_number = models.CharField(max_length=100)
    card_expire = models.CharField(max_length=100)
    recurrent = models.BooleanField(default=False)
    verify = models.BooleanField(default=False)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.card_number

