from django.db import models

from apps.basic.models import Specialist
from apps.service.models.service import WorkTime


class Booked(models.Model):
    user = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)
    worktime = models.ForeignKey(WorkTime, on_delete=models.CASCADE, blank=True, null=True)
