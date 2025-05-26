from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.basic.serializers.comment import CommentSerializer, CommentCreateSerializer
from api.basic.serializers.specialist import SpecialistSerializers
from api.basic.views.specialist import SmallPagesPagination
from api.clinic.serializers.clinic import ClinicSerializers, ClinicServiceSerializers, SpecialistServiceSerializers, \
    CommentServiceSerializers, ClinicDetailSerializers
from apps.basic.models import Specialist
from apps.clinic.models import Clinic, Service
from apps.clinic.models.comment import Comment
from apps.users.model import Patient


class CommentView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = ClinicDetailSerializers

    def get_queryset(self):
        clinic_id = self.kwargs.get('clinic_id')
        return Comment.objects.filter(clinic__id=clinic_id)


class ClinicServiceDetailView(ListAPIView):
    serializer_class = ClinicServiceSerializers

    def get_queryset(self):
        clinic_id = self.kwargs.get('clinic_id')
        return Service.objects.filter(clinic__id=clinic_id)


class SpecialistServiceDetailView(ListAPIView):
    serializer_class = SpecialistSerializers

    def get_queryset(self):
        clinic_id = self.kwargs.get('clinic_id')
        return Specialist.objects.filter(staff__id=clinic_id)


class CommentServiceDetailView(ListAPIView):
    serializer_class = CommentServiceSerializers

    def get_queryset(self):
        clinic_id = self.kwargs.get('clinic_id')
        return Comment.objects.filter(clinic__id=clinic_id)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request):
    data = request.data.copy()
    data['author'] = Patient.objects.filter(user=request.user).last().id
    data['date'] = timezone.now()
    serializer = CommentCreateSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

