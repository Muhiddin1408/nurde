from django.db import models

from apps.basic.models import Specialist
from apps.clinic.models import Clinic, Symptom
from apps.service.models.service import Service
from apps.users.model import Patient, Address, Ankita
from apps.utils.models import Category


class Phone(models.Model):
    phone = models.CharField(max_length=12, unique=True)


class OrderFile(models.Model):
    file = models.FileField(upload_to='orders/')


class Order(models.Model):
    STATUS_CHOICES = (
        ('wait', 'wait'),
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('cancellation', 'cancellation'),
    )
    customer = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)
    payment_type = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='wait')
    datetime = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    image = models.ManyToManyField(OrderFile, blank=True, null=True)
    ankita = models.ForeignKey(Ankita, on_delete=models.CASCADE, blank=True, null=True)
    service = models.ManyToManyField(Service, blank=True, null=True)
    phone = models.ManyToManyField(Phone, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    clinic = models.ForeignKey(Clinic, blank=True, null=True, on_delete=models.CASCADE)
    recomment = models.BooleanField(default=False)


class Diagnosis(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    date = models.DateField(auto_now_add=True)
    comment = models.TextField()


class Recommendations(models.Model):
    diagnosis = models.ManyToManyField(Symptom, blank=True, null=True)
    recommendation = models.TextField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    result = models.TextField(blank=True, null=True)


