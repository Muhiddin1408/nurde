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
        request = self.request
        clinic = request.user.specialist.adminclinic.clinic

        filters = {'clinic': clinic}

        status = request.GET.get('status')
        if status:
            filters['status'] = status

        date = request.GET.get('date')
        if date:
            filters['datetime__date'] = date

        if filters:
            return Order.objects.filter(**filters)

        return Order.objects.none()