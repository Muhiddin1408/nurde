from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.basic.serializers.specialist import SpecialistSerializers
from api.basic.views.specialist import SmallPagesPagination
from apps.basic.models import AdminClinic, Worker
from doctor.clinic.serializers.worker import WorkerSerializer


class WorkerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status_param = request.query_params.get('status')
        user = request.user.specialist

        admin = AdminClinic.objects.filter(specialist=user, status=True).last()
        if not admin:
            return Response({"error": "Admin topilmadi yoki status noto‘g‘ri"}, status=404)

        clinic = admin.clinic
        queryset = Worker.objects.filter(clinic=clinic)

        if status_param is not None:
            queryset = queryset.filter(status=status_param)

        paginator = SmallPagesPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = WorkerSerializer(page, many=True, context={"request": request})

        return paginator.get_paginated_response(serializer.data)