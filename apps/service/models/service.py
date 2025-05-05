from django.db import models

from apps.basic.models import Specialist
from apps.users.model.weekday import Weekday
from apps.utils.models import Category


class WorkTime(models.Model):
    user = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    weekday = models.ForeignKey(Weekday, on_delete=models.CASCADE)
    date = models.TimeField(blank=True, null=True)
    finish = models.TimeField(blank=True, null=True)


class Service(models.Model):
    user = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    preparation = models.CharField(max_length=100, blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


