from rest_framework import viewsets

from api.clinic.serializers.clinic import ClinicSerializers
from apps.clinic.models import Clinic


class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializers