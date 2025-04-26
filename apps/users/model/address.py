from django.db import models

from apps.users.model.patient import Patient


class Address(models.Model):
    name = models.CharField(max_length=100)
    street = models.CharField(max_length=100, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    entrance = models.IntegerField(blank=True, null=True)
    floor = models.IntegerField(blank=True, null=True)
    no = models.CharField(max_length=125,blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    lat = models.FloatField()
    lng = models.FloatField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Адреса'
        verbose_name = 'Адреса'
