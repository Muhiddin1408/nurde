from django.db import models

from apps.users.model import Patient


class Relative(models.Model):
    name = models.CharField(max_length=100)


class ImageAnkita(models.Model):
    file = models.FileField(upload_to='orders/')


class Ankita(models.Model):
    GEN = (
        ('man', "MAN"),
        ('woman', "WOMAN"),
    )
    name = models.CharField(max_length=100)
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    relative = models.ForeignKey(Relative, on_delete=models.CASCADE)
    birthday = models.DateField()
    gen = models.CharField(max_length=125, choices=GEN)
    height = models.IntegerField()
    weight = models.IntegerField()
    phone = models.CharField(max_length=100, blank=True, null=True)
    # image = models.ForeignKey(ImageAnkita, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
