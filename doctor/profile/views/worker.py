from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.basic.views.specialist import SmallPagesPagination
from apps.basic.models import Worker
from doctor.profile.serializers.worker import WorkerDoctorSerializer


class WorkerViewSet(APIView):

    def get(self, request):
        status_param = request.query_params.get('status')
        user = request.user.specialist
        queryset = Worker.objects.filter(specialist=user, status=status_param)
        paginator = SmallPagesPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = WorkerDoctorSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)


class WorkerDoctorCreat(APIView):
    def post(self, request):
        user = request.user.specialist
        clinic_id = request.data['clinic']
        Worker.objects.create(clinic_id=clinic_id, specialist=user)
        return Response({"msg": "created"}, status=status.HTTP_201_CREATED)
