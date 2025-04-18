from django.urls import path

from api.auth.views.login import login
from api.auth.views.registration import RegisterView, sms_conf

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login, name='login'),
    path('sms_conf/', sms_conf, name='sms_conf'),
]