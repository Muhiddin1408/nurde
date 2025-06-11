from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.utils.serializsers.story import StorySerializer
from apps.utils.models.story import Story, StoryView


class StoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status = self.request.query_params.get('type')
        stories = Story.objects.filter(status=status)
        serializer = StorySerializer(stories, many=True, context={'request': request})
        return Response(serializer.data)
