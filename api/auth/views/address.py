from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.auth.serializers.address import AddressSerializer
from apps.users.model import Address, Patient


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            patient = Patient.objects.filter(user=user).first()
            if patient:
                return Address.objects.filter(patient=patient).order_by('-id')
        return Address.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        patient = Patient.objects.get(user=user)
        serializer.save(patient=patient)
