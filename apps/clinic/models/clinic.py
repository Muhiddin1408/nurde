from django.db import models


class Clinic(models.Model):
    TYPE = (
        ('clinic', 'clinic'),
        ('laboratories', 'laboratories'),
        ('diagnostic_centers', 'diagnostic_centers'),
    )
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="clinics/")
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    license = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=TYPE, default='clinic')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиники'
        verbose_name_plural = 'Клиники'


