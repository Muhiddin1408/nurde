from payme.classes.client import Payme
from rest_framework import viewsets, permissions, status, generics
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from api.basic.views.specialist import SmallPagesPagination
from api.order.serializers.order import MyOrderSerializers, OrderSerializers, OrderFileSerializer, DiagnosisSerializers, \
    MyOrderListSerializers
from apps.order.models import Order, OrderFile, Diagnosis
from apps.users.model import Patient


class MyOrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = MyOrderListSerializers
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SmallPagesPagination

    def get_queryset(self):
        user = self.request.user
        status = self.request.query_params.get('status', None)
        queryset = Order.objects.filter(customer=Patient.objects.filter(user=user).last()).order_by('-id')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response(MyOrderSerializers(instance, context={'request': request}).data)





class OrderViewSet(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Order saqlanadi
        # user = Patient.objects.filter(user=request.user.id).last()
        order = serializer.save()

        # Payme bilan to'lov havolasini yaratish
        # payme = Payme(payme_id="6830068ddfc9ac0473674de8")  # <-- o'zingizning `payme_id` ni kiriting
        # pay_link = payme.initializer.generate_pay_link(
        #     id=order.id,
        #     amount=order.amount,
        # )

        # Javobni qaytarish (order va payme link bilan)
        return Response({
            'order_id': order.id,
            'amount': order.amount,
            # 'pay_link': pay_link
        }, status=status.HTTP_201_CREATED)


class ImageViewSet(ListAPIView):
    queryset = OrderFile.objects.all()
    serializer_class = OrderFileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        file = request.data['file']
        image = OrderFile.objects.create(file=file)
        return Response({'id':image.id}, status=status.HTTP_201_CREATED)


class DiagnosisViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs.get('pk')

        try:
            diagnosis = Diagnosis.objects.get(id=pk)
        except Diagnosis.DoesNotExist:
            return None

        if diagnosis.order.customer.user == user:
            return Diagnosis.objects.filter(id=pk)  # yoki kerakli queryset
        return None



