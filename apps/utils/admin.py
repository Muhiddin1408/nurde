from django.contrib import admin

from apps.utils.models import Category
from apps.utils.models.like import Like
from apps.utils.models.story import Story

# Register your models here.
admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Story)
