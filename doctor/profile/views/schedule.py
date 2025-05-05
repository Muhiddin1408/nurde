from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.basic.serializers.specialist import WorkTimeSerializer
from apps.basic.models import Specialist
from apps.service.models.service import WorkTime
from doctor.profile.serializers.schedule import MyScheduleSerializer


class MyScheduleView(generics.ListAPIView):
    queryset = WorkTime.objects.all()
    serializer_class = MyScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        work_times = WorkTime.objects.filter(user__user=user)
        return work_times

