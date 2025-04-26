from django.db import models

from apps.users.model.patient import Patient


class Address(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    entrance = models.CharField(max_length=125,blank=True, null=True)
    floor = models.CharField(max_length=125,blank=True, null=True)
    number = models.CharField(max_length=125,blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Адреса'
        verbose_name = 'Адреса'
