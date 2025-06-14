from django.urls import path

from doctor.clinic.views.change_worker import ChangeWorker
from doctor.clinic.views.clinic_doctor import AdminClinicDoctorView
from doctor.clinic.views.schedule import WorkTimeCreateClinicView
from doctor.clinic.views.worker import WorkerView

urlpatterns = [
    path('admin/create/', AdminClinicDoctorView.as_view(), name='admin-create'),
    path('specialist/', WorkerView.as_view(), name='clinic-specialist'),
    path('work/', WorkTimeCreateClinicView.as_view(), name='clinic-specialist'),
    path('change/status/', ChangeWorker.as_view(), name='change-status'),
]