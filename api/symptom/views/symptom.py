from rest_framework import viewsets, filters

from api.symptom.serializers.symptom import SymptomSerializers
from apps.clinic.models import Symptom


class SymptomView(viewsets.ReadOnlyModelViewSet):
    queryset = Symptom.objects.filter(type='symptom')
    serializer_class = SymptomSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', 'name_ru', 'name_en')


class DiagnosesView(viewsets.ReadOnlyModelViewSet):
    queryset = Symptom.objects.filter(type='diagnoses')
    serializer_class = SymptomSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', 'name_ru', 'name_en')
