from django.db import models

from apps.users.models import User


class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    c_lat = models.IntegerField(null=True, blank=True)
    c_lon = models.IntegerField(null=True, blank=True)
    pol = models.CharField(max_length=25)

