from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from api.basic.serializers.service import ServiceSerializers
from apps.clinic.models import Service
from apps.utils.models import Category


class ServiceView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = ServiceSerializers
    search_fields = ['name']
    queryset = Category.objects.all()
    filter_backends = [filters.SearchFilter]