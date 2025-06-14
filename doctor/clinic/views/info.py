from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor.clinic.serializers.info import ClinicSerializers


class ClinicInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        clinic = request.user.specialist
        ser = ClinicSerializers(clinic, context={'request': request})
        return Response(ser.data)
