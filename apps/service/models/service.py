from django.db import models

from apps.basic.models import Specialist
from apps.clinic.models import Clinic
from apps.users.model.weekday import Weekday
from apps.utils.models import Category


class WorkTime(models.Model):
    user = models.ForeignKey(Specialist, on_delete=models.CASCADE, blank=True, null=True, related_name='worktime_specialist')
    weekday = models.ForeignKey(Weekday, on_delete=models.CASCADE)
    date = models.TimeField(blank=True, null=True)
    finish = models.TimeField(blank=True, null=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, blank=True, null=True,)


class Service(models.Model):
    STATUS_CHOICES = (
        ('active', 'active'),
        ('process', 'process'),
        ('reject', 'reject')
    )
    user = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    preparation = models.CharField(max_length=100, blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, default='active', choices=STATUS_CHOICES)

    def __str__(self):
        return str(self.preparation) + ' ---' + str(self.description) + ' --' + str(self.category.name) + ' ' + str(self.price)


