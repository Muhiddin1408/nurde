from rest_framework import generics, permissions

from api.basic.views.specialist import SmallPagesPagination
from api.order.serializers.order import OrderSerializers, MyOrderSerializers
from apps.order.models import Order


class DashboardView(generics.ListAPIView):
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