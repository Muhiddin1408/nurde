from django.contrib import admin

from apps.users.model.chat import ChatRoom, Message, MessageDoctor, ChatDoctor
from apps.users.model.weekday import Weekday
from apps.users.models import User
from apps.users.model import Address, Patient, Ankita, Relative, Image

# Register your models here.

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Patient)
admin.site.register(Weekday)
admin.site.register(Ankita)
admin.site.register(Relative)
admin.site.register(Image)
admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(MessageDoctor)
admin.site.register(ChatDoctor)

