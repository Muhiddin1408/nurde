from django.db import models

from apps.basic.models import Specialist
from apps.users.model import Patient, Address


class Order(models.Model):
    customer = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)
    payment_type = models.CharField(max_length=20)
