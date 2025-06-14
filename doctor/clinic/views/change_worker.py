from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.basic.models import Worker
from doctor.clinic.serializers.change import ImageSerializer


class ChangeWorker(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self, request):
        data = request.data
        specialist_id = data.get('id')
        new_status = data.get('status')


        if not specialist_id or new_status is None:
            return Response({"error": "ID yoki status yuborilmadi"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            worker = Worker.objects.filter(specialist_id=specialist_id).last()
            if worker.clinic.id != request.user.specialist.adminclinic.clinic.id:
                return Response({"error": "Admin Xato"})
            if not worker:
                return Response({"error": "Worker topilmadi"}, status=status.HTTP_404_NOT_FOUND)

            worker.status = new_status
            worker.save()

            return Response({"msg": "Worker holati muvaffaqiyatli o'zgartirildi"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ImageCreateAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # Rasm yuklash uchun kerak

    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)