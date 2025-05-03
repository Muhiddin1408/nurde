from django.db import models

from apps.basic.models import Specialist


class Education(models.Model):
    TYPE_CHOICES = (
        ('education', 'Education'),
        ('advanced', 'Advanced')
    )
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    name = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    start_date = models.IntegerField(null=True, blank=True)
    finish = models.IntegerField()
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)


class FileEducation(models.Model):
    file = models.FileField(upload_to='education')
    education = models.ForeignKey(Education, on_delete=models.CASCADE, related_name='file_education', blank=True, null=True)

