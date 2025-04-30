from datetime import timedelta, datetime

import random
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.utils.eskiz import SendSmsApiWithEskiz
from apps.users.models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def forget(request):
    try:
        username = request.data['username']
        user = User.objects.filter(username=username, is_staff=True).last()
        if user:
            sms_code = random.randint(1000, 9999)
            user = User.objects.get(username=username)
            user.sms_code = sms_code
            user.save()
            SendSmsApiWithEskiz(message="https://star-one.uz/ Tasdiqlash kodi " + str(sms_code),
                                phone=int(username)).send()
            return Response({'status': True}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'status': f'{e}'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny, ])
def sms_forget(request):
    try:
        sms_code = request.data['code']
        phone = request.data['username']
        user = User.objects.filter(username=phone, is_staff=True).last()
        result = {
            'code': False,
        }
        if user and int(user.sms_code) == int(sms_code):
            result = {
                'code': True,
            }
            return Response(result, status=status.HTTP_200_OK)
        return Response(result, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny, ])
def password_forget(request):
    try:
        phone = request.data['username']
        password = request.data['password']
        user = User.objects.get(username=phone, is_staff=True)

        result = {
            'access': None,
            'refresh': None,
        }
        if user:
            user.set_password(password)
            user.is_active = True
            user.save()
            token = RefreshToken.for_user(user)
            result = {
                'access': str(token.access_token),
                'refresh': str(token)
            }
        return Response(result, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
