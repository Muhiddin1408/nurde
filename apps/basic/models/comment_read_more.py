from django.db import models

from apps.basic.models import Specialist
from apps.basic.models.read_more import ReadMore
from apps.order.models import Order
from apps.users.model import Patient
from apps.users.models import User


class CommentReadMore(models.Model):
    ranking = models.IntegerField(default=0)
    comment = models.TextField()
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)
    service_rendered = models.DateField(blank=True, null=True)
    experts_response = models.CharField(max_length=255, blank=True, null=True)
    read_more = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.comment + " "

    class Meta:
        verbose_name_plural = 'Комментарий'
        verbose_name = 'Комментарий'


class CommentReadMoreLike(models.Model):
    comment = models.ForeignKey(CommentReadMore, on_delete=models.CASCADE)
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)


class CommentReadMoreComment(models.Model):
    parent = models.ForeignKey(CommentReadMore, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


