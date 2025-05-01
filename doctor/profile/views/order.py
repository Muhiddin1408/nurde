from rest_framework import generics, permissions

from api.basic.views.specialist import SmallPagesPagination
from api.order.serializers.order import MyOrderSerializers
from apps.order.models import Order


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