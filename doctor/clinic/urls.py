from django.urls import path

from doctor.clinic.views.change_worker import ChangeWorker, ImageCreateAPIView
from doctor.clinic.views.clinic_doctor import AdminClinicDoctorView
from doctor.clinic.views.info import ClinicInfo, DoctorInfo
from doctor.clinic.views.schedule import WorkTimeCreateClinicView, WorkTimeDoctorClinicView
from doctor.clinic.views.worker import WorkerView

urlpatterns = [
    path('admin/create/', AdminClinicDoctorView.as_view(), name='admin-create'),
    path('specialist/', WorkerView.as_view(), name='clinic-specialist'),
    path('work/', WorkTimeCreateClinicView.as_view(), name='clinic-specialist'),
    path('doctor/time/', WorkTimeDoctorClinicView.as_view(), name='clinic-specialist'),
    path('change/status/', ChangeWorker.as_view(), name='change-status'),
    path('image/', ImageCreateAPIView.as_view(), name='image'),
    path('info/', ClinicInfo.as_view(), name='clinic-info'),
    path('time/doctor/', DoctorInfo.as_view(), name='clinic-info'),
]