from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.users.serializers.message import MessageSerializer
from apps.users.model.chat import Message


class MessageViewSet(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     user = self.request.user
    #     room =

