from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.basic.serializers.specialist import SpecialistSerializers
from apps.basic.models import AdminClinic, Worker
from doctor.clinic.serializers.worker import WorkerSerializer


class WorkerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status_param = request.query_params.get('status')
        user = request.user.specialist

        admin = AdminClinic.objects.filter(user=user, status=True).last()

        if admin:
            clinic = admin.clinic
            if status_param == 'active':
                worker = Worker.objects.filter(clinic=clinic)
                serializer = WorkerSerializer(worker, context={"request": request})
                return Response(serializer.data)



        return Response({"error": "Admin topilmadi yoki status noto‘g‘ri"}, status=404)