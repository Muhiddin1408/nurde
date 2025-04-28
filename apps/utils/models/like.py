from django.db import models

from apps.basic.models import Specialist
from apps.clinic.models import Clinic
from apps.users.model import Patient


class Like(models.Model):
    user = models.ForeignKey(Specialist, on_delete=models.CASCADE, blank=True, null=True)
    costumer = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
