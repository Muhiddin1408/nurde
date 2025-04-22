from django.db import models

from apps.basic.models import Specialist
from apps.users.model.weekday import Weekday


class InWork(models.Model):
    weekday = models.ForeignKey(Weekday, on_delete=models.CASCADE)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    start = models.TimeField()
    finish = models.TimeField()
