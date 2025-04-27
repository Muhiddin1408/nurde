from django.db import models

from apps.clinic.models.symptom import Symptom
from apps.utils.models import Category


class SymptomType(models.Model):
    TYPE_CHOICES = (
        ('review', "Review"),
        ('reasons', "Reasons"),
        ('treatment', "Treatment"),
        ('treats', "Treats")
    )
    name = models.CharField(max_length=100)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.name


class SymptomSubType(models.Model):
    name = models.CharField(max_length=100)
    symptom = models.ForeignKey(SymptomType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
