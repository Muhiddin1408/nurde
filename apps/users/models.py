from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=120)
    sms_code = models.IntegerField(blank=True, null=True)
    sms_code_time = models.DateTimeField(blank=True, null=True)
    sms_status = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'


