from django.db import models
from parler.models import TranslatableModel, TranslatedFields


# from apps.clinic.models import Clinic


class Category(models.Model):
    name = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    icon = models.FileField(upload_to='icon/', blank=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    # class Meta:
    #     verbose_name_plural = 'Категории'
    #     verbose_name = 'Категории'