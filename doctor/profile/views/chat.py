from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.basic.models import Specialist
from apps.users.model.chat import ChatDoctor, MessageDoctor
from doctor.profile.serializers.chat import MessageDoctorSerializer


class MessageViewSet(generics.ListCreateAPIView):
    queryset = MessageDoctor.objects.all()
    serializer_class = MessageDoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        room = ChatDoctor.objects.filter(parent=Specialist.objects.filter(user=user).last())
        if room.exists():
            return MessageDoctor.objects.filter(room=room.last())
        else:
            return MessageDoctor.objects.none()