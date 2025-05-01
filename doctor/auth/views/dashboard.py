from rest_framework import generics, permissions

from api.basic.views.specialist import SmallPagesPagination
from apps.basic.models import Specialist
from apps.clinic.models import Clinic
from doctor.auth.serializers.dashboard import DashboardSerializer


class DashboardView(generics.RetrieveAPIView):
    queryset = Specialist.objects.all()
    serializer_class = DashboardSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SmallPagesPagination

    def get_object(self):
        clinic = Specialist.objects.filter(user=self.request.user).last()
        if clinic:
            return clinic
        return None