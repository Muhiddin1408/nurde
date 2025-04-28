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
        # Faqat o'zi (request.user) ga tegishli patientni qaytaradi
        status = self.request.query_params.get('type')
        return Like.objects.filter(costumer=Patient.objects.filter(user=self.request.user).last(), user__isnull=False)

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        if not user_id:
            return Response({'detail': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Kim like qilmoqda
        costumer = Patient.objects.filter(user=request.user).last()

        # Avval bazada bormi tekshiramiz
        like = Like.objects.filter(costumer=costumer, user_id=user_id).first()

        if like:
            like.delete()
            return Response({'detail': 'Like removed'}, status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
