from django.db import models

from apps.users.model import Patient


class Relative(models.Model):
    name = models.CharField(max_length=100)


class Ankita(models.Model):
    GEN = (
        ('man', "MAN"),
        ('woman', "WOMAN"),
    )
    name = models.CharField(max_length=100)
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)
    relative = models.ForeignKey(Relative, on_delete=models.CASCADE)
    birthday = models.DateField()
    gen = models.CharField(max_length=125, choices=GEN)
    height = models.IntegerField()
    weight = models.IntegerField()
    phone = models.IntegerField()
    def __str__(self):
        return self.name
