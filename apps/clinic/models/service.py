from django.db import models

from apps.clinic.models.clinic import Clinic
from apps.utils.models.category import Category


class Service(models.Model):

    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services', blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    preparation = models.CharField(max_length=100, blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Услуги'
        verbose_name_plural = 'Услуги'
