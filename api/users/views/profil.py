from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound, APIException, NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.users.serializers.profile import ProfileUpdateSerializer
from apps.users.model import Patient


class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user

        # Foydalanuvchi tekshiruvi
        if not user or not user.is_authenticated:
            raise NotAuthenticated("Avval tizimga kiring.")

        try:
            # Kerak bo‘lsa select_related bilan optimallashtirish
            patient = Patient.objects.select_related("user").get(user=user)
            # Agar object-level permissionlar bo‘lsa, shu yerda tekshirish mumkin:
            # self.check_object_permissions(self.request, patient)
            return patient
        except Patient.DoesNotExist:
            # Faqat o‘zi (request.user) ga tegishli patient topilmadi
            raise NotFound("Ushbu foydalanuvchiga tegishli patient topilmadi.")

        except Patient.MultipleObjectsReturned:
            # Noto‘g‘ri ma’lumotlar holati: bitta bo‘lishi kerak edi.
            # Xohlasangiz eng so‘nggisini qaytarib turishingiz mumkin,
            # yoki darhol xatolik ko‘taring. Quyida aniq xatolik ko‘tariladi:
            raise APIException(
                "Ichki xatolik: ushbu foydalanuvchi uchun bir nechta patient yozuvi mavjud."
            )


