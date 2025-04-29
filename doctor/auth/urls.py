from django.urls import path

from doctor.auth.views.auth import SpecialistRegister, SpecialistUpdate, password_conf

urlpatterns = [
    path('register/', SpecialistRegister.as_view(), name='register'),
    path('password_conf/', password_conf, name='password_conf_doctor'),
    path('update/', SpecialistUpdate.as_view(), name='update'),
]