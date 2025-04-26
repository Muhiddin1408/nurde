from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response

from api.order.serializers.order import MyOrderSerializers, OrderSerializers
from apps.order.models import Order


class MyOrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = MyOrderSerializers
    permission_classes = [permissions.IsAuthenticated]


class OrderViewSet(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    permission_classes = [permissions.IsAuthenticated]



