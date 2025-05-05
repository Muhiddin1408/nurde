from rest_framework import generics

from apps.service.models.service import WorkTime


class MyScheduleView(generics.ListAPIView):
    queryset = WorkTime.objects.all()