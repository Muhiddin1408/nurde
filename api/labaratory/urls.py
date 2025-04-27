from django.urls import path
from rest_framework.routers import SimpleRouter

from api.labaratory.views.labaratory import ClinicViewSet, CommentView, ClinicServiceDetailView, \
    SpecialistServiceDetailView

router = SimpleRouter()
router.register(r'', ClinicViewSet)

urlpatterns = [
    path('<int:clinic_id>/comment/', CommentView.as_view(), name='clinic-detail'),
    path('<int:clinic_id>/services/', ClinicServiceDetailView.as_view(), name='clinic-services'),
    # path('<int:clinic_id>/specialist/', SpecialistServiceDetailView.as_view()),
] + router.urls

