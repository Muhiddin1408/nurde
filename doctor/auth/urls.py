from django.urls import path

from doctor.auth.views.auth import SpecialistRegister, SpecialistUpdate

urlpatterns = [
    path('register/', SpecialistRegister.as_view(), name='register'),
    path('update/', SpecialistUpdate.as_view(), name='register'),
]