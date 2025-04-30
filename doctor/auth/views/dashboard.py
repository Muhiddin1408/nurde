from rest_framework import generics, permissions

from apps.basic.models import Specialist
from apps.clinic.models import Clinic
from doctor.auth.serializers.dashboard import DashboardSerializer


class DashboardView(generics.ListAPIView):
    queryset = Clinic.objects.all()
    serializer_class = DashboardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        clinic = Specialist.objects.filter(user=self.request.user).last().staff
        if clinic:
            return clinic.staff.all()
        return None