from django.db import models

from apps.clinic.models.clinic import Clinic
from apps.utils.models.category import Category


class Service(models.Model):
    type = models.CharField(max_length=50)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, related_name='services')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Услуги'
        verbose_name_plural = 'Услуги'
