from django.db import models

from apps.clinic.models import Clinic
from apps.users.models import User


class Comment(models.Model):
    comment = models.TextField()
    date = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    ranking = models.IntegerField(default=0)

    def __str__(self):
        return self.comment