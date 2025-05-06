from rest_framework import viewsets, generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from api.basic.views.specialist import SmallPagesPagination
from api.users.serializers.favorite import LikeSerializer
from apps.users.model import Patient
from apps.utils.models.like import Like


class FavoriteDoctorViewSet(generics.ListCreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SmallPagesPagination

    def get_queryset(self):
        status = self.request.query_params.get('type')
        if status == 'doctor':
            return Like.objects.filter(costumer=Patient.objects.filter(user=self.request.user).last(), user__isnull=False)
        elif status == 'clinic':
            return Like.objects.filter(costumer=Patient.objects.filter(user=self.request.user).last(), clinic__isnull=False)
        else:
            return Like.objects.none()

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        clinic = request.data.get('clinic')

        # Kim like qilmoqda
        costumer = Patient.objects.filter(user=request.user).last()

        # Avval bazada bormi tekshiramiz
        if user_id:
            like = Like.objects.filter(costumer=costumer, user_id=user_id).first()
        elif clinic:
            like = Like.objects.filter(costumer=costumer, clinic_id=clinic).first()
        else:
            like = Like.objects.filter(costumer=costumer, clinic_id=clinic).first()

        if like:
            like.delete()
            return Response({'detail': 'Like removed'})
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
