from django.db import models

from apps.basic.models import Specialist
from apps.utils.models import Category


class Work(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    finish = models.IntegerField(blank=True, null=True)
    start = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class WorkImage(models.Model):
    file = models.FileField(upload_to='education')
    education = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='file_word', blank=True,
                                  null=True)
