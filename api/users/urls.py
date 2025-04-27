from django.urls import path
from rest_framework.routers import DefaultRouter

from api.users.views.ankita import AnkitaView, RelativeView
from api.users.views.profil import ProfileUpdateView

router = DefaultRouter()
router.register(r'ankita', AnkitaView)
router.register(r'relative', RelativeView)
urlpatterns = [
    path('', ProfileUpdateView.as_view(), name='profile'),

] + router.urls
