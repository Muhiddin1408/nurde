from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=120, blank=True, null=True)
    sms_code = models.IntegerField(blank=True, null=True)
    sms_code_time = models.DateTimeField(blank=True, null=True)
    sms_status = models.BooleanField(default=False)
    passport = models.CharField(blank=True, null=True, max_length=255)
    pin = models.IntegerField(blank=True, null=True)
    middle_name = models.CharField(blank=True, null=True, max_length=255)
    lang = models.CharField(blank=True, null=True, max_length=255)
    is_active = models.BooleanField(default=False)
    birth_day = models.DateField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)


    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'


