from django.db import models

from apps.order.models import Order
from apps.users.models import User


class Payment(models.Model):
    STATUS = (
        ('doctor', 'doctor'),
        ('user', 'user')
    )
    amount = models.FloatField()
    status = models.CharField(max_length=50, choices=STATUS, default='user')
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + " " + str(self.amount) + " " + str(self.status)
