from django.db import models

from apps.clinic.models import Clinic


class Image(models.Model):
    image = models.FileField(upload_to='images/')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=False)
