from django.views import generic
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from api.utils.serializsers.image import ImageSerializer
from apps.order.models import OrderFile
from apps.users.model import Image


class ImageViewSet(ListAPIView):
    queryset = OrderFile.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        file = request.data['file']
        image = OrderFile.objects.create(image=file)
        return Response(ImageSerializer(image).data)