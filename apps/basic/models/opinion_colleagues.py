from django.db import models

from apps.basic.models.read_more import ReadMore
from apps.basic.models.specialists import Specialist


class OpinioColleague(models.Model):
    comment = models.TextField()
    opinion = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    read_more = models.ForeignKey(ReadMore, on_delete=models.CASCADE)

    def __str__(self):
        return self.opinion.user.last_name + " " + self.comment
