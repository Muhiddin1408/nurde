from django.db import models

from apps.clinic.models.type import TypeClinic


class Clinic(models.Model):
    TYPE = (
        ('clinic', 'clinic'),
        ('laboratories', 'laboratories'),
        ('diagnostic_centers', 'diagnostic_centers'),
    )
    CATEGORY_CHOICES = (
        ('private', 'private'),
        ('state', 'state')
    )
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    license = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=TYPE, default='clinic')
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='private')
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    types = models.ForeignKey(TypeClinic, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    # class Meta:
    #     verbose_name = 'Клиники'
    #     verbose_name_plural = 'Клиники'


