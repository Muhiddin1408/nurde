from django.db import models

from apps.basic.models.specialists import Specialist


class ReadMore(models.Model):
    name = models.CharField(max_length=100)
    service_prices = models.IntegerField()
    experience = models.IntegerField()
    education = models.CharField(max_length=100)
    qualifications = models.CharField(max_length=100)
    associations = models.CharField(max_length=100)
    specialists = models.ForeignKey(Specialist, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " " + self.specialists.user.last_name
