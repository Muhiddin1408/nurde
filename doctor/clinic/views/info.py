from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.basic.models import AdminClinic
from apps.service.models.service import WorkTime
from doctor.clinic.serializers.info import ClinicSerializers
from doctor.profile.serializers.schedule import WorkTimeSerializer


class ClinicInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        clinic = request.user.specialist
        admin = AdminClinic.objects.filter(specialist=clinic).first()
        ser = ClinicSerializers(admin.clinic, context={'request': request})
        return Response(ser.data)


class DoctorInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        specialist_id = request.query_params.get('specialist')
        clinic = request.user.specialist
        admin = AdminClinic.objects.filter(specialist=clinic).first()
        work = WorkTime.objects.filter(user_id=specialist_id, clinic=admin.clinic)
        return Response(WorkTimeSerializer(work, many=True).data)
