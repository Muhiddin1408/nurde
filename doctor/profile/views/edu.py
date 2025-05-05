from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.basic.models.education import Education, FileEducation
from doctor.profile.serializers.edu import EducationSerializer, FileEducationSerializer


class EducationListCreateView(generics.ListCreateAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = IsAuthenticated


class EducationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = IsAuthenticated


class FileEducationListCreateView(generics.CreateAPIView):
    queryset = FileEducation.objects.all()
    serializer_class = FileEducationSerializer

