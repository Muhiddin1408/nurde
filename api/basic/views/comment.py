from django.db.models import OuterRef, Exists
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.basic.serializers.comment import MyCommentSerializer, WaitCommentSerializers
from api.basic.serializers.info import CommentReadMoreSerializer
from api.basic.views.specialist import SmallPagesPagination
from apps.basic.models import CommentReadMore
from apps.order.models import Order
from apps.users.model import Patient


class CommentViewSet(generics.ListAPIView):
    queryset = CommentReadMore.objects.all()
    serializer_class = MyCommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SmallPagesPagination

    def get_queryset(self):
        user = self.request.user
        return CommentReadMore.objects.filter(user=Patient.objects.filter(user=user).first())


class WaitCommentViewSet(generics.ListAPIView):
    queryset = Order.objects.filter(status='waiting')
    serializer_class = WaitCommentSerializers
    permission_classes = [IsAuthenticated]
    pagination_class = SmallPagesPagination

    def get_queryset(self):
        user = self.request.user
        comments = CommentReadMore.objects.filter(
            user__user=user,  # Patient orqali userga kirilmoqda
            order=OuterRef('pk')
        )

        # Orderlar: Shu userga tegishli, lekin hali comment yozilmaganlar
        orders_without_comment = Order.objects.filter(
            customer__user=user  # Order.user -> Patient, Patient.user -> user
        ).annotate(
            has_comment=Exists(comments)
        ).filter(
            has_comment=False
        )
        return orders_without_comment

