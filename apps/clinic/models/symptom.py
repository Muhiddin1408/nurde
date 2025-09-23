from django.db import models


class Symptom(models.Model):
    TYPE_CHOICES = (
        ('symptom', 'Symptom'),
        ('diagnoses', 'Diagnoses'),
    )
    name = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name
