from django.urls import path
from rest_framework.routers import DefaultRouter

from api.users.views.ankita import AnkitaView, RelativeView

router = DefaultRouter()
router.register(r'ankita', AnkitaView)
router.register(r'relative', RelativeView)
urlpatterns = [

] + router.urls
