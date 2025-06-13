from django.db import models

from apps.clinic.models import Clinic
from apps.users.models import User


# class ClinicUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     clinic = models.OneToOneField(Clinic, on_delete=models.CASCADE)
#     is_active = models.BooleanField(default=False)