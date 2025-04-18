from django.db import models

from apps.clinic.models.clinic import Clinic
from apps.utils.models.category import Category


class Service(models.Model):
    image = models.ImageField(upload_to='service', blank=True, null=True)
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=255, blank=True, null=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, related_name='services')

    class Meta:
        verbose_name = 'Услуги'
        verbose_name_plural = 'Услуги'
