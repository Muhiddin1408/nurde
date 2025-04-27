from rest_framework import viewsets
from rest_framework.generics import ListAPIView

from api.basic.serializers.specialist import SpecialistSerializers
from api.basic.views.specialist import SmallPagesPagination
from api.clinic.serializers.clinic import ClinicSerializers, CommentServiceSerializers, ClinicServiceSerializers, \
    ClinicDetailSerializers
from apps.basic.models import Specialist
from apps.clinic.models import Clinic, Comment, Service


class ClinicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Clinic.objects.filter(type='laboratories')
    serializer_class = ClinicSerializers
    pagination_class = SmallPagesPagination


class CommentView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = ClinicDetailSerializers

    def get_queryset(self):
        clinic_id = self.kwargs.get('clinic_id')
        return Comment.objects.filter(clinic__id=clinic_id)


class ClinicServiceDetailView(ListAPIView):
    serializer_class = ClinicServiceSerializers

    def get_queryset(self):
        clinic_id = self.kwargs.get('clinic_id')
        return Service.objects.filter(clinic__id=clinic_id)


class SpecialistServiceDetailView(ListAPIView):
    serializer_class = SpecialistSerializers

    def get_queryset(self):
        clinic_id = self.kwargs.get('clinic_id')
        return Specialist.objects.filter(staff__id=clinic_id)


class CommentServiceDetailView(ListAPIView):
    serializer_class = CommentServiceSerializers

    def get_queryset(self):
        clinic_id = self.kwargs.get('clinic_id')
        return Comment.objects.filter(clinic__id=clinic_id)
