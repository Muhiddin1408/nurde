from rest_framework import generics, permissions

from apps.basic.models import Specialist
from doctor.auth.serializers.auth import SpecialistSerializer, SpecialistUpdateSerializer


class SpecialistRegister(generics.CreateAPIView):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer


class IsActiveUserOrAny(permissions.BasePermission):
    """
    Custom permission to allow inactive users to access the view.
    """
    def has_permission(self, request, view):
        # Allow access for both active and inactive users
        return True


class SpecialistUpdate(generics.UpdateAPIView):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveUserOrAny]

    def get_object(self):
        print(self.request.user)
        return Specialist.objects.filter(user=self.request.user).last()

