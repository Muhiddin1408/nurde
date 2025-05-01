from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.basic.views.specialist import SmallPagesPagination
from api.order.serializers.order import MyOrderSerializers
from apps.order.models import Order
from apps.service.models.booked import Booked


class OrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = MyOrderSerializers
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SmallPagesPagination

    def get_queryset(self):
        status = self.request.GET.get('status')
        if status:
            return Order.objects.filter(doctor__user=self.request.user, status=status)
        return Order.objects.none()

class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = MyOrderSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Faqatgina ushbu foydalanuvchiga tegishli buyurtmalarni ko‘rsatish
        return Order.objects.filter(doctor__user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def confirm(request):
    data = request.data
    order_id = data.get('order')
    action_type = data.get('type')

    if not order_id or not action_type:
        return Response({'detail': 'order and type are required'}, status=status.HTTP_400_BAD_REQUEST)

    order = get_object_or_404(Order, pk=order_id, doctor__user=request.user)

    if action_type == 'active':
        order.status = 'active'
        Booked.objects.create(user=order.doctor, date=order.datetime)
    elif action_type == 'cancel':
        order.status = 'cancellation'
    else:
        return Response({'detail': 'Invalid type. Must be "active" or "cancel".'}, status=status.HTTP_400_BAD_REQUEST)

    order.save()
    return Response({'detail': 'Order status updated successfully'}, status=status.HTTP_200_OK)




