from rest_framework import viewsets

from api.basic.views.specialist import SmallPagesPagination
from api.clinic.serializers.clinic import ClinicSerializers
from apps.clinic.models import Clinic


class ClinicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Clinic.objects.filter(type='clinic')
    serializer_class = ClinicSerializers
    pagination_class = SmallPagesPagination
