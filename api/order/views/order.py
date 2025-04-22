from rest_framework import viewsets, permissions

from api.order.serializers.order import MyOrderSerializers
from apps.order.models import Order


class MyOrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = MyOrderSerializers
    permission_classes = [permissions.IsAuthenticated]