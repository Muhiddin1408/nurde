from django.db import models

from apps.clinic.models.clinic import Clinic
from apps.users.models import User
from apps.utils.models.category import Category


# Create your models here.


class Specialist(models.Model):
    TYPE_CHOICES = (
        ('nurses', "nurses"),
        ('doctor', "doctor"),
    )
    TYPE_SERVICE = (
        ('online', "online"),
        ('offline', "offline"),
        ('night', "night"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    photo = models.ImageField(upload_to='specialists/%Y/%m/%d/', blank=True)
    category = models.ManyToManyField(Category, blank=True)
    experience = models.IntegerField(default=0)
    type_service = models.CharField(max_length=100, choices=TYPE_SERVICE)
    staff = models.ManyToManyField(Clinic)

    def __str__(self):
        return self.type + " - " + str(self.user)
