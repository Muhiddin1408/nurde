from django.db import models

# from apps.clinic.models import Clinic


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категории'