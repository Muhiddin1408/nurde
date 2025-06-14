from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.basic.models import AdminClinic
from doctor.clinic.serializers.info import ClinicSerializers


class ClinicInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        clinic = request.user.specialist
        admin = AdminClinic.objects.filter(specialist=clinic).first()
        ser = ClinicSerializers(admin.clinic, context={'request': request})
        return Response(ser.data)
