from django.urls import path
from rest_framework.routers import SimpleRouter

from doctor.auth.views.auth import SpecialistRegister, SpecialistUpdate, password_conf, CategoryView, login, sms_conf, \
    LoginWithSocialDoctorViewSet
from doctor.auth.views.dashboard import DashboardView
from doctor.auth.views.forget import forget, sms_forget, password_forget
from doctor.auth.views.profile import ProfileView

router = SimpleRouter()
router.register('google', LoginWithSocialDoctorViewSet, 'doctor-google')

urlpatterns = [
    path('register/', SpecialistRegister.as_view(), name='register'),
    path('password_conf/', password_conf),
    path('update/', SpecialistUpdate.as_view(), name='update'),
    path('category/', CategoryView.as_view(), name='category'),
    path('login/', login, name='login_doctor'),
    path('profile/', ProfileView.as_view(), name='profile_doctor'),
    path('dashboard/', DashboardView.as_view(), name='dashboard_doctor'),
    path('sms_conf/', sms_conf),

    path('forget/', forget, name='forget'),
    path('sms_forget/', sms_forget, name='sms_forget'),
    path('password_forget/', password_forget, name='password_forget'),
]