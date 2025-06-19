from django.db import models

from apps.users.models import User


class Balance(models.Model):
    balance = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.balance) + " " + str(self.user)
