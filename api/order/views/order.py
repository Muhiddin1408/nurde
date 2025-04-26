from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from api.order.serializers.order import MyOrderSerializers, OrderSerializers
from apps.order.models import Order


class MyOrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = MyOrderSerializers
    permission_classes = [permissions.IsAuthenticated]


class OrderViewSet(viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

