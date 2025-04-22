from django.contrib import admin

from apps.clinic.models import Clinic, InfoClinic, Service, Description, Photo, Symptom, SymptomType, SymptomSubType
from apps.clinic.models.comment import Comment


# Register your models here.

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(InfoClinic)
admin.site.register(Service)
admin.site.register(Comment)
admin.site.register(Description)
admin.site.register(Photo)

admin.site.register(Symptom)
admin.site.register(SymptomType)
admin.site.register(SymptomSubType)
