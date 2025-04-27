from rest_framework import viewsets, permissions, status, generics
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from api.order.serializers.order import MyOrderSerializers, OrderSerializers, OrderFileSerializer
from apps.order.models import Order, OrderFile
from apps.users.model import Patient


class MyOrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = MyOrderSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        status = self.request.query_params.get('status', None)
        queryset = Order.objects.filter(customer=Patient.objects.filter(user=user).last()).order_by('-id')
        if status:
            queryset = queryset.filter(status=status)
        return queryset



class OrderViewSet(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    permission_classes = [permissions.IsAuthenticated]


class ImageViewSet(ListAPIView):
    queryset = OrderFile.objects.all()
    serializer_class = OrderFileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        file = request.data['file']
        image = OrderFile.objects.create(file=file)
        return Response({'id':image.id}, status=status.HTTP_201_CREATED)



