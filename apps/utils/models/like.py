from django.db import models

from apps.basic.models import Specialist
from apps.users.model import Patient


class Like(models.Model):
    user = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    costumer = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
