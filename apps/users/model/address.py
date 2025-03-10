from django.db import models

from apps.users.model.patient import Patient


class Address(models.Model):
    name = models.CharField(max_length=100)
    street = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    home = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    lat = models.FloatField()
    lng = models.FloatField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Адреса'
        verbose_name = 'Адреса'
