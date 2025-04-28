from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.users.serializers.message import MessageSerializer
from apps.users.model import Patient
from apps.users.model.chat import Message, ChatRoom


class MessageViewSet(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        room = ChatRoom.objects.filter(parent=Patient.objects.filter(user=user).last())
        if room.exists():
            return Message.objects.filter(room=room.last())
        else:
            return Message.objects.none()
