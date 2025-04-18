from django.urls import path

from api.auth.views.login import login
from api.auth.views.registration import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login, name='login'),
]