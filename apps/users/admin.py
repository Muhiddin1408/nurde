from django.contrib import admin

from apps.users.models import User
from apps.users.model import Address, Patient

# Register your models here.

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Patient)
