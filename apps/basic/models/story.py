from django.db import models

from apps.users.models import User


# Create your models here.


class Story(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='story/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + " - " + str(self.user)
