from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.basic.models import Specialist, AdminClinic
from apps.clinic.models import Clinic
from doctor.auth.serializers.profile import ProfileSerializer, AdminClinicSerializers


class ProfileView(generics.RetrieveAPIView):
    queryset = Specialist.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return Specialist.objects.get(user=user)


class CreateAdminClinicView(APIView):

    def post(self, request):
        specialist = request.user.specialist  # yoki yuqoridagi .first() bilan
        clinic_id = request.data.get('clinic_id')

        try:
            clinic = Clinic.objects.get(id=clinic_id)
        except Clinic.DoesNotExist:
            return Response({"detail": "Clinic not found."}, status=404)

        admin_clinic = AdminClinic.objects.create(
            specialist=specialist,
            clinic=clinic,
            status=True
        )

        serializer = AdminClinicSerializers(admin_clinic)
        return Response(serializer.data, status=201)

