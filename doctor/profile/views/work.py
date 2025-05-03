from rest_framework import generics

from apps.basic.models.work import Work, WorkImage
from doctor.profile.serializers.work import WorkSerializer, FileWorkSerializer


class WorkListCreateView(generics.ListCreateAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer


class WorkRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer


class FileWorkListCreateView(generics.CreateAPIView):
    queryset = WorkImage.objects.all()
    serializer_class = FileWorkSerializer
