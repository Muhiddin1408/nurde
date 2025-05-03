from rest_framework import generics, permissions

from api.basic.serializers.info import CommentReadMoreSerializer
from api.basic.serializers.ranking import RankingSerializer
from apps.basic.models import CommentReadMore, Specialist


class CommentView(generics.ListAPIView):
    queryset = CommentReadMore.objects.all()
    serializer_class = CommentReadMoreSerializer

    def get_queryset(self):
        user = self.request.user
        comment = CommentReadMore.objects.filter(read_more=Specialist.objects.get(user=user))
        return comment


class RankingView(generics.RetrieveAPIView):
    queryset = Specialist.objects.all()
    serializer_class = RankingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Specialist.objects.get(user=self.request.user)
