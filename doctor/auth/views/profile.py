from rest_framework import generics, permissions

from apps.basic.models import Specialist
from doctor.auth.serializers.profile import ProfileSerializer


class ProfileView(generics.RetrieveAPIView):
    queryset = Specialist.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return Specialist.objects.get(user=user)

