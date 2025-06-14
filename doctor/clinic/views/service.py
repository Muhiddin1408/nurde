from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.clinic.models import Service
from doctor.clinic.serializers.service import ServiceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'specialist') and hasattr(user.specialist, 'adminclinic'):
            clinic = user.specialist.adminclinic.clinic
            return Service.objects.filter(clinic=clinic)
        return Service.objects.none()

    def perform_create(self, serializer):
        clinic = self.request.user.specialist.adminclinic.clinic
        serializer.save(clinic=clinic, status='process')

    def perform_update(self, serializer):
        serializer.save(status='process')
