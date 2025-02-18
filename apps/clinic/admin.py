from django.contrib import admin

from apps.clinic.models import Clinic, InfoClinic, Service, Description, Photo


# Register your models here.

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(InfoClinic)
admin.site.register(Service)
admin.site.register(Description)
admin.site.register(Photo)
