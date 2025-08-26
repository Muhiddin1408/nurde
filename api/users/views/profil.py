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
            raise NotAuthenticated("Please log in to access this resource.")

        try:
            patient = Patient.objects.select_related("user").get(user=user)
            return patient
        except Patient.DoesNotExist:
            raise NotFound("No patient found for the current user.")

        except Patient.MultipleObjectsReturned:
            raise APIException(
                "Internal error: multiple patient records found for this user."
            )


