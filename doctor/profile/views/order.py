from datetime import datetime

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
        order = Order.objects.filter(doctor__user=self.request.user, status=status)
        if order:
            return order
        return None

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
    order = Order.objects.get(pk=data['order'])
    type = data['type']
    if type == 'active':
        order.status = 'active'
        Booked.objects.create(user=order.user, date=order.datetime)
    elif type == 'cancel':
        order.status = 'cancellation'
    order.save()
    return Response(status=status.HTTP_200_OK)




