from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.order.serializers.order import MyOrderSerializers
from apps.order.models import Order


class AnkitaHistoryViewSet(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(ankita_id=kwargs['pk'])
        serializer = MyOrderSerializers(order, many=True, context={'request': request})
        return Response(serializer.data)
