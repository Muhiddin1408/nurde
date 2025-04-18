from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.users.model import Patient
from apps.users.models import User


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # yoki AllowAny, agar ro'yxatdan o'tish vaqtida bo‘lsa
def update_user_info(request):
    pinfl = request.data.get('pin')
    birth_date = request.data.get('birth_date')

    if not all([pinfl, birth_date]):
        return Response({'msg': 'pin and birth_date are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = request.user
        Patient.objects.create(user=user, birth_date=birth_date, pinfl=pinfl)
        return Response({'detail': 'User info updated successfully.'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)