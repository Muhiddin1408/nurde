from django.contrib import admin
from .models import Specialist, ReadMore, CommentReadMore, Story, OpinionColleague, AdminClinic, Worker, Balance, \
    Payment
from .models.education import Education
from .models.in_work import InWork
from .models.payme import Payme
from .models.work import Work

# Register your models here.

admin.site.register(Specialist)
admin.site.register(Balance)
admin.site.register(CommentReadMore)
admin.site.register(Payment)
admin.site.register(OpinionColleague)
admin.site.register(Education)
admin.site.register(InWork)
admin.site.register(Work)
admin.site.register(AdminClinic)
admin.site.register(Worker)
admin.site.register(Payme)
