from rest_framework.generics import RetrieveAPIView, ListAPIView
from api.clinic.serializers.clinic import ClinicSerializers, ClinicServiceSerializers, SpecialistServiceSerializers, \
    CommentServiceSerializers
from apps.basic.models import Specialist
from apps.clinic.models import Clinic, Service
from apps.clinic.models.comment import Comment


class ClinicDetailView(RetrieveAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializers


class ClinicServiceDetailView(ListAPIView):
    serializer_class = ClinicServiceSerializers

    def get_queryset(self):
        clinic_id = self.kwargs.get('clinic_id')
        return Service.objects.filter(clinic__id=clinic_id)


class SpecialistServiceDetailView(ListAPIView):
    serializer_class = SpecialistServiceSerializers

    def get_queryset(self):
        clinic_id = self.kwargs.get('clinic_id')
        return Specialist.objects.filter(clinic__id=clinic_id)


class CommentServiceDetailView(ListAPIView):
    serializer_class = CommentServiceSerializers

    def get_queryset(self):
        clinic_id = self.kwargs.get('clinic_id')
        return Comment.objects.filter(clinic__id=clinic_id)
