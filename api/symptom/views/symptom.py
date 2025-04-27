from rest_framework import viewsets

from api.symptom.serializers.symptom import SymptomSerializers
from apps.clinic.models import Symptom


class SymptomView(viewsets.ReadOnlyModelViewSet):
    queryset = Symptom.objects.filter(type='symptom')
    serializer_class = SymptomSerializers


class DiagnosesView(viewsets.ReadOnlyModelViewSet):
    queryset = Symptom.objects.filter(type='diagnoses')
    serializer_class = SymptomSerializers
