from django.db import models


class TimeMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True
