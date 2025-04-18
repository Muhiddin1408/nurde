from django.urls import path
from rest_framework.routers import DefaultRouter

from api.auth.views.address import AddressViewSet
from api.auth.views.login import login
from api.auth.views.registration import RegisterView, sms_conf, password_conf
router = DefaultRouter()
router.register(r'addresses', AddressViewSet, basename='address')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login, name='login'),
    path('sms_conf/', sms_conf, name='sms_conf'),
    path('password_conf/', password_conf, name='password_conf'),
] + router.urls
