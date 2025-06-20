from django.db import models


class Payme(models.Model):
    id_name = models.CharField(max_length=1000, blank=True, null=True)
    crated_at = models.IntegerField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    method = models.CharField(max_length=1000, blank=True, null=True)
    cancel_at = models.IntegerField(blank=True, null=True)
    perform_time = models.IntegerField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)