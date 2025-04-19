from django.db import models

from apps.basic.models import Specialist
from apps.basic.models.read_more import ReadMore
from apps.users.model import Patient
from apps.users.models import User


class CommentReadMore(models.Model):
    ranking = models.IntegerField(default=0)
    comment = models.TextField()
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)
    service_rendered = models.DateField(blank=True, null=True)
    experts_response = models.CharField(max_length=255, blank=True, null=True)
    read_more = models.ForeignKey(Specialist, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment + " " + self.user.last_name

    class Meta:
        verbose_name_plural = 'Комментарий'
        verbose_name = 'Комментарий'

