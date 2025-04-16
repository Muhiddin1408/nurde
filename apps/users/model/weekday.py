from django.db import models


class Weekday(models.Model):
    name = models.CharField(max_length=50)
