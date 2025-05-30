from django.db import models

from apps.users.models import User


class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    latitude = models.IntegerField(null=True, blank=True)
    longitude = models.IntegerField(null=True, blank=True)
    pol = models.CharField(max_length=25, blank=True, null=True)
    pinfl = models.CharField(max_length=125, blank=True, null=True)
    image = models.ImageField(upload_to='patients/', blank=True, null=True)


    class Meta:
        verbose_name = 'Пациенты'
        verbose_name_plural = 'Пациенты'
