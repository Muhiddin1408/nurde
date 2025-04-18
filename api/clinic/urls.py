
from django.urls import path
from rest_framework.routers import SimpleRouter

from api.clinic.views.clinic import ClinicViewSet
from api.clinic.views.clinic_detail import ClinicDetailView, ClinicServiceDetailView, SpecialistServiceDetailView
router = SimpleRouter()
router.register(r'clinics', ClinicViewSet)

urlpatterns = [
    # path('clinic/', ClinicViewSet.as_view(), name='clinic'),
    path('clinics/<int:pk>/', ClinicDetailView.as_view(), name='clinic-detail'),
    path('clinics/<int:clinic_id>/services/', ClinicServiceDetailView.as_view(), name='clinic-services'),
    path('clinics/<int:clinic_id>/specialist/', SpecialistServiceDetailView.as_view(), name='clinic-services'),
] + router.urls