from rest_framework import viewsets, permissions

from api.basic.serializers.service import ServiceSerializer
from apps.service.models.service import Service


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return
        return Service.objects.none()