from rest_framework import viewsets
from rest_framework.views import APIView

from api.order.serializers.order import MyOrderSerializers
from apps.order.models import Order


class AnkitaHistoryViewSet(APIView):
    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(ankita_id=kwargs['pk'])
        return MyOrderSerializers(order, many=True).data
