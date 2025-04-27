from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.users.serializers.profile import ProfileUpdateSerializer
from apps.users.model import Patient


class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        print(self.request.user.last_name)
        # Faqat o'zi (request.user) ga tegishli patientni qaytaradi
        return Patient.objects.get(user=self.request.user)


