from django.db import models

from apps.basic.models import Specialist


class Education(models.Model):
    TYPE_CHOICES = (
        ('education', 'Education'),
        ('advanced', 'Advanced')
    )
    type = models.CharField(max_length=125)
    name = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    start = models.IntegerField(null=True, blank=True)
    finish = models.IntegerField(blank=True, null=True)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)


class FileEducation(models.Model):
    file = models.FileField(upload_to='education')
    education = models.ForeignKey(Education, on_delete=models.CASCADE, related_name='file_education', blank=True, null=True)

