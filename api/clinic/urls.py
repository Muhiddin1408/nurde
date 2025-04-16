from django.urls import path

from api.clinic.views.clinic_detail import ClinicDetailView, ClinicServiceDetailView, SpecialistServiceDetailView

urlpatterns = [
    path('clinics/<int:pk>/', ClinicDetailView.as_view(), name='clinic-detail'),
    path('clinics/<int:clinic_id>/services/', ClinicServiceDetailView.as_view(), name='clinic-services'),
    path('clinics/<int:clinic_id>/specialist/', SpecialistServiceDetailView.as_view(), name='clinic-services'),
]