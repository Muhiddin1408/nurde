from django.contrib import admin
from .models import Specialist, ReadMore, CommentReadMore, Story, OpinionColleague
from .models.education import Education
from .models.in_work import InWork

# Register your models here.

admin.site.register(Specialist)
# admin.site.register(ReadMore)
admin.site.register(CommentReadMore)
admin.site.register(Story)
admin.site.register(OpinionColleague)
admin.site.register(Education)
admin.site.register(InWork)
