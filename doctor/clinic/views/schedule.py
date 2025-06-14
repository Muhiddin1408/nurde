from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.service.models.service import WorkTime
from doctor.profile.serializers.schedule import WorkTimeBulkWrapperSerializer, WorkTimeSerializer, \
    WorkTimeBulkClinicSerializer


class WorkTimeCreateClinicView(generics.CreateAPIView):
    queryset = WorkTime.objects.all()
    serializer_class = WorkTimeBulkClinicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_worktimes = serializer.save()
        return Response({
            "success": True,
            "data": WorkTimeSerializer(created_worktimes, many=True, context=self.get_serializer_context()).data
        }, status=status.HTTP_201_CREATED)