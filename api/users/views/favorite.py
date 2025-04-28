from rest_framework import viewsets, generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from api.basic.views.specialist import SmallPagesPagination
from api.users.serializers.favorite import LikeSerializer
from apps.users.model import Patient
from apps.utils.models.like import Like


class FavoriteDoctorViewSet(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SmallPagesPagination

    def get_queryset(self):
        # Faqat o'zi (request.user) ga tegishli patientni qaytaradi
        status = self.request.query_params.get('type')
        return Like.objects.filter(costumer=Patient.objects.filter(user=self.request.user), user__isnull=True)

    def delete(self, request, *args, **kwargs):
        like_id = request.data.get('id')  # id ni body ichidan olamiz

        if not like_id:
            return Response(
                {"error": "id kiritilmagan."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            like = self.get_queryset().get(id=like_id)
        except Like.DoesNotExist:
            raise NotFound("Bunday Like topilmadi.")

        like.delete()

        return Response(
            {"message": "Like muvaffaqiyatli o'chirildi."},
            status=status.HTTP_204_NO_CONTENT
        )
