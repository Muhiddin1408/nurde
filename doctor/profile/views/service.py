from rest_framework import viewsets, generics, permissions

from api.basic.serializers.service import ServiceSerializer, ServiceUpdateSerializer
from apps.basic.models import Specialist
from apps.service.models.service import Service


class ServiceViewSet(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Service.objects.filter(user=Specialist.objects.get(user=user))


class ServiceDetail(generics.RetrieveUpdateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]


