from django.urls import path
from rest_framework.routers import DefaultRouter

from api.users.views.ankita import AnkitaView, RelativeView
from api.users.views.favorite import FavoriteDoctorViewSet
from api.users.views.message import MessageViewSet
from api.users.views.profil import ProfileUpdateView

router = DefaultRouter()
router.register(r'ankita', AnkitaView)
router.register(r'relative', RelativeView)
urlpatterns = [
    path('', ProfileUpdateView.as_view(), name='profile'),
    path('favorite/', FavoriteDoctorViewSet.as_view(), name='favorite'),
    path('message/', MessageViewSet.as_view(), name='message'),

] + router.urls
