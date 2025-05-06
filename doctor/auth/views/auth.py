from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
import random

from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken

from api.auth.serializers.register import RegisterSerializer
from api.auth.views.registration import is_all_digits
from api.utils.eskiz import SendSmsApiWithEskiz
from api.utils.gmail_sms import send_verification_email
from apps.basic.models import Specialist
from apps.users.models import User
from apps.utils.models import Category
from doctor.auth.serializers.auth import SpecialistSerializer, SpecialistUpdateSerializer, CategorySerializer


class SpecialistRegister(generics.CreateAPIView):

    permission_classes = [AllowAny, ]
    # throttle_scope = "authentication"
    throttle_classes = [ScopedRateThrottle, ]

    @swagger_auto_schema(
        tags=['authentication'],
        request_body=RegisterSerializer,
        responses={201: RegisterSerializer}
    )
    def post(self, request):
        phone = request.data.get('username')
        user = User.objects.filter(username='d' + phone).last()
        if user is None:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            sms_code = random.randint(1000, 9999)
            user = User.objects.get(username='d' + phone)
            user.sms_code = sms_code
            user.save()
            if is_all_digits(phone):
                SendSmsApiWithEskiz(message="https://star-one.uz/ Tasdiqlash kodi " + str(sms_code),
                                    phone=int(phone)).send()
            else:
                send_verification_email(phone, sms_code)
            return Response({'status': False}, status=status.HTTP_200_OK)
        elif not user.is_active or not user.is_staff:
            sms_code = random.randint(1000, 9999)
            user = User.objects.get(username='d' + phone)
            user.sms_code = sms_code
            user.save()
            if is_all_digits(phone):
                SendSmsApiWithEskiz(message="https://star-one.uz/ Tasdiqlash kodi " + str(sms_code),
                                    phone=int(phone)).send()

            # else:
            #     send_verification_email(phone, sms_code)
            return Response({'status': False}, status=status.HTTP_200_OK)
        else:
            return Response({'status': True}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_conf(request):
    try:
        required_fields = ['username', 'password', 'last_name', 'first_name', 'gender']
        missing_fields = [field for field in required_fields if field not in request.data]
        if missing_fields:
            raise ValidationError(f"Fields {', '.join(missing_fields)} are required.")

        phone = request.data['username']
        password = request.data['password']
        last_name = request.data['last_name']
        first_name = request.data['first_name']
        gender = request.data['gender']

        middle_name = request.data.get('middle_name')
        birth_day = request.data.get('date_of_birth')
        passport = request.data.get('passport')

        user = User.objects.get(username='d' + phone)
        user.is_active = True
        user.is_staff = True
        user.last_name = last_name
        user.first_name = first_name
        user.middle_name = middle_name
        user.gen = gender
        user.birth_day = birth_day
        user.set_password(password)
        user.save()

        Specialist.objects.get_or_create(
            user=user,
            defaults={'password': password, 'pinfl': passport}
        )

        token = RefreshToken.for_user(user)
        return Response({
            'access': str(token.access_token),
            'refresh': str(token)
        }, status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError as ve:
        return Response({"detail": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SpecialistUpdate(generics.UpdateAPIView):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Specialist.objects.filter(user=self.request.user).last()


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@api_view(['POST'])
@permission_classes([AllowAny, ])
def login(request):
    try:
        phone = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username='d' + phone, is_staff=True).first()
        doctor = Specialist.objects.filter(user=user, password=password).first()
        if doctor:
            user.save()
            token = RefreshToken.for_user(user)
            result = {
                'access': str(token.access_token),
                'refresh': str(token),
            }

            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({'msg': "Username or password incorrect"}, status=status.HTTP_404_NOT_FOUND)

    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please set all reqiured fields'
        }
        return Response(res)


