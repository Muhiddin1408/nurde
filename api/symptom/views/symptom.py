from rest_framework import viewsets

from api.symptom.serializers.symptom import SymptomSerializers
from apps.clinic.models import Symptom


class SymptomView(viewsets.ReadOnlyModelViewSet):
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializers
