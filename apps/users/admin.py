from django.contrib import admin

from apps.users.model.weekday import Weekday
from apps.users.models import User
from apps.users.model import Address, Patient

# Register your models here.

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Patient)
admin.site.register(Weekday)
