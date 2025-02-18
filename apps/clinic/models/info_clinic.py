from django.db import models

from apps.clinic.models.clinic import Clinic
from apps.utils.models import Category


class InfoClinic(models.Model):
    website = models.URLField(max_length=500)
    management = models.CharField(max_length=500)
    price_services = models.CharField(max_length=500)
    clinic_name = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.clinic_name


class Description(models.Model):
    description = models.CharField(max_length=500)
    info_clinic = models.ForeignKey(InfoClinic, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class Photo(models.Model):
    parent = models.ForeignKey(InfoClinic, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos')

    def __str__(self):
        return self.parent.clinic_name.name
