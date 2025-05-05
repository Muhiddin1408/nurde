from rest_framework import viewsets, generics, permissions

from api.basic.serializers.service import ServiceSerializer, ServiceUpdateSerializer
from api.basic.serializers.specialist import CategorySerializer
from apps.basic.models import Specialist
from apps.service.models.service import Service
from apps.utils.models import Category


class ServiceViewSet(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Service.objects.filter(user=Specialist.objects.get(user=user))



class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]


class MyCategoryViewSet(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        doctor = Specialist.objects.get(user=user)
        return doctor.category.all()


