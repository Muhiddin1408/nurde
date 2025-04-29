from rest_framework import generics, permissions

from apps.basic.models import Specialist
from doctor.auth.serializers.auth import SpecialistSerializer, SpecialistUpdateSerializer


class SpecialistRegister(generics.CreateAPIView):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer


class SpecialistUpdate(generics.UpdateAPIView):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Specialist.objects.filter(user=self.request.user).last()

