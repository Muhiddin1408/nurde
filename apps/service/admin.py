from django.contrib import admin

from apps.service.models.booked import Booked
from apps.service.models.service import WorkTime


# Register your models here.
@admin.register(WorkTime)
class WorkTimeAdmin(admin.ModelAdmin):
    list_display = ('date',)


@admin.register(Booked)
class BookedAdmin(admin.ModelAdmin):
    list_display = ('date',)

