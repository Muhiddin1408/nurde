from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated

from apps.basic.models import Specialist
from apps.service.models.service import WorkTime
from apps.users.model import Weekday
from doctor.profile.serializers.schedule import MyScheduleSerializer, WeekdaySerializer, WorkTimeSerializer, \
    WorkTimeBulkWrapperSerializer


class WeekdayView(generics.ListAPIView):
    queryset = Weekday.objects.all()
    serializer_class = WeekdaySerializer


class WorkTimeCreateView(generics.CreateAPIView):
    queryset = WorkTime.objects.all()
    serializer_class = WorkTimeBulkWrapperSerializer
    permission_classes = [permissions.IsAuthenticated]


class MyScheduleView(generics.ListAPIView):
    queryset = WorkTime.objects.all()
    serializer_class = MyScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        work_times = WorkTime.objects.filter(user__user=user)
        return work_times


class MyScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkTime.objects.all()
    serializer_class = MyScheduleSerializer
    permission_classes = [IsAuthenticated]

