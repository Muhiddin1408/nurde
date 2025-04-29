from django.urls import path

from doctor.auth.views.auth import SpecialistRegister, SpecialistUpdate, password_conf, CategoryView, login

urlpatterns = [
    path('register/', SpecialistRegister.as_view(), name='register'),
    path('password_conf/', password_conf, name='password_conf_doctor'),
    path('update/', SpecialistUpdate.as_view(), name='update'),
    path('category/', CategoryView.as_view(), name='category'),
    path('login/', login, name='login_doctor'),
]