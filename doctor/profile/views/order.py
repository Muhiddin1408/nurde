from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.basic.views.specialist import SmallPagesPagination
from api.order.serializers.order import MyOrderSerializers
from apps.clinic.models import Symptom
from apps.order.models import Order, Diagnosis, Recommendations
from apps.service.models.booked import Booked


class OrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = MyOrderSerializers
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SmallPagesPagination

    def get_queryset(self):
        status = self.request.GET.get('status')
        date = self.request.GET.get('date')
        if status:
            if date:
                return Order.objects.filter(doctor__user=self.request.user, status=status, datetime__date=date)
            return Order.objects.filter(doctor__user=self.request.user, status=status)
        if date:
            return Order.objects.filter(doctor__user=self.request.user, datetime__date=date)
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
    action_type = data.get('status')
    print(order_id)
    print(action_type)

    if not order_id or not action_type:
        return Response({'detail': 'order and status are required'}, status=status.HTTP_400_BAD_REQUEST)

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


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create(request):
    data = request.data
    order_id = data.get('order')
    result = data.get('result')
    recommendations = data.get('recommendation')
    diagnosis = data.get('diagnosis', [])

    if not order_id:
        return Response({'detail': 'order is required'}, status=status.HTTP_400_BAD_REQUEST)

    order = get_object_or_404(Order, pk=order_id, doctor__user=request.user)

    # Create Recommendations
    recommendations = Recommendations.objects.create(
        order=order,
        recommendation=recommendations,
        result=result
    )

    # Add diagnosis to Recommendations
    if diagnosis:
        try:
            diagnosis_ids = list(map(int, diagnosis))
            symptoms = Symptom.objects.filter(pk__in=diagnosis_ids, type='diagnoses')
            recommendations.diagnosis.set(symptoms)
        except ValueError:
            return Response({'detail': 'Diagnosis must be a list of integers'}, status=status.HTTP_400_BAD_REQUEST)
        symptoms = Symptom.objects.filter(pk__in=diagnosis)
        recommendations.diagnosis.set(symptoms)
        symptoms = Symptom.objects.filter(pk__in=diagnosis)
        recommendations.diagnosis.set(symptoms)

    recommendations.save()

    order.status = 'inactive'
    order.save()

    return Response({'detail': 'Recommendation created successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def comment(request):
    data = request.data
    order_id = data.get('order')
    comment = data.get('comment')

    if not order_id:
        return Response({'detail': 'order is required'}, status=status.HTTP_400_BAD_REQUEST)

    order = get_object_or_404(Order, pk=order_id, doctor__user=request.user)
    Diagnosis.objects.create(order=order, comment=comment, diagnosis=comment)

    # order.status = 'inactive'
    # order.save()

    return Response({'detail': 'Order completed successfully'}, status=status.HTTP_200_OK)





