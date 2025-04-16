from django.db import models

from apps.basic.models import Specialist
from apps.users.model.weekday import Weekday


class WorkTime(models.Model):
    user = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    weekday = models.ForeignKey(Weekday, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)

