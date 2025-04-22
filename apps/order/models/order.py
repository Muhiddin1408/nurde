from django.db import models

from apps.basic.models import Specialist
from apps.users.model import Patient, Address


class Order(models.Model):
    STATUS_CHOICES = (
        ('active', 'active'),
        ('inactive', 'inactive'),
    )
    customer = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)
    payment_type = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    datetime = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    file = models.FileField(upload_to='orders/', blank=True, null=True)
    image = models.ImageField(upload_to='orders/', blank=True, null=True)

