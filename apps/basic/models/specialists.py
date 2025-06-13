from django.db import models

from apps.clinic.models.clinic import Clinic
from apps.users.models import User
from apps.utils.models.category import Category


# Create your models here.


class Specialist(models.Model):
    TYPE_CHOICES = (
        ('nurses', "nurses"),
        ('doctor', "doctor"),
        ('clinic', "clinic"),
    )
    TYPE_SERVICE = (
        ('online', "online"),
        ('offline', "offline"),
        ('night', "night"),
    )
    GEN = (
        ('man', 'man'),
        ('woman', 'woman'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, blank=True, null=True)
    photo = models.ImageField(upload_to='specialists/%Y/%m/%d/', blank=True)
    category = models.ManyToManyField(Category, blank=True, null=True)
    experience = models.IntegerField(default=0)
    type_service = models.CharField(max_length=100, choices=TYPE_SERVICE, blank=True, null=True)
    staff = models.ManyToManyField(Clinic, blank=True, null=True)
    info = models.TextField(blank=True)
    pinfl = models.CharField(max_length=100, blank=True)
    gen = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.user.last_name + "  " + self.user.first_name + " " + self.user.username


    class Meta:
        verbose_name = 'Специалисты'
        verbose_name_plural = 'Специалисты'


class AdminClinic(models.Model):
    TYPE_CHOICES = (
        ('admin', "admin"),
        ('director', "director"),
        ('manager', "manager"),
        ('sub_director', "sub_director"),
    )
    specialist = models.OneToOneField(Specialist, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    type = models.CharField(max_length=100, blank=True, null=True, choices=TYPE_CHOICES)
    phone = models.IntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)


class Worker(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
