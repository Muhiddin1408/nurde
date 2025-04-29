import random
from datetime import timedelta, datetime

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import validate_email
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.auth.serializers.register import RegisterSerializer, PasswordSerializers
from api.utils.eskiz import SendSmsApiWithEskiz
from api.utils.gmail_sms import send_verification_email
from apps.users.model import Patient
from apps.users.models import User


def is_all_digits(value):
    if isinstance(value, str):
        return value.isdigit()
    return False

class RegisterView(APIView):
    permission_classes = [AllowAny,]
    # throttle_scope = "authentication"
    throttle_classes = [ScopedRateThrottle,]

    @swagger_auto_schema(
        tags=['authentication'],
        request_body=RegisterSerializer,
        responses={201: RegisterSerializer}
    )
    def post(self, request):
        phone = request.data.get('username')
        user = User.objects.filter(username=phone).last()
        if user is None:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            sms_code = random.randint(1000, 9999)
            user = User.objects.get(username=phone)
            user.sms_code = sms_code
            user.save()
            if is_all_digits(phone):
                SendSmsApiWithEskiz(message="https://star-one.uz/ Tasdiqlash kodi " + str(sms_code),
                            phone=int(phone)).send()
            else:
                send_verification_email(phone, sms_code)
            return Response({'status': False},status=status.HTTP_200_OK)
        elif not user.is_active:
            sms_code = random.randint(1000, 9999)
            user = User.objects.get(username=phone)
            user.sms_code = sms_code
            user.sms_code_time = datetime.now() + timedelta(minutes=2)
            user.save()
            if is_all_digits(phone):
                SendSmsApiWithEskiz(message="https://star-one.uz/ Tasdiqlash kodi " + str(sms_code),
                                    phone=int(phone)).send()

            # else:
            #     send_verification_email(phone, sms_code)
            return Response({'status': False},status=status.HTTP_200_OK)
        else:
            return Response({'status': True}, status=status.HTTP_200_OK)
#

# @api_view(['POST'])
# @permission_classes([AllowAny, ])
# def register(request):
#     try:
#         phone = request.data['username']
#         user = User.objects.get(username=phone)
#         result = {
#             'access': None,
#             'refresh': None,
#         }
#         if User.objects.filter(username=phone).exists():
#             result = {
#                 'username': user.username,
#             }
#         else:
#
#         return Response(result, status=status.HTTP_200_OK)
#     except:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([AllowAny, ])
def sms_conf(request):
    try:
        sms_code = request.data['code']
        phone = request.data['username']
        user = User.objects.filter(username=phone).last()

        result = {
            'code': False,
        }
        if user and int(user.sms_code) == int(sms_code):
            result = {
                'code': True
            }
            return Response(result, status=status.HTTP_200_OK)
        return Response(result, status=status.HTTP_200_OK)

    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_conf(request):
    try:
        required_fields = ['username', 'password', 'passport', 'date_of_birth']
        for field in required_fields:
            if field not in request.data:
                raise ValidationError(f"{field} is required.")

        phone = request.data['username']
        password = request.data['password']
        passport = request.data['passport']
        date_of_birth = request.data['date_of_birth']

        try:
            data = datetime.strptime(date_of_birth, "%d.%m.%Y").date()
        except ValueError:
            return Response({"detail": "date_of_birth must be in DD.MM.YYYY format."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(username=phone)

        user.set_password(password)
        user.passport = passport
        user.is_active = True
        user.save()

        if not Patient.objects.filter(user=user).exists():
            Patient.objects.create(user=user, date_of_birth=data, pinfl=passport)

        token = RefreshToken.for_user(user)
        result = {
            'access': str(token.access_token),
            'refresh': str(token)
        }

        return Response(result, status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError as ve:
        return Response({"detail": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([AllowAny, ])
# def register(request):
#     try:
#         phone = request.data.get('phone')
#         if not phone:
#             res = {
#                 'msg': 'Login empty',
#                 'status': 0,
#             }
#             return Response(res)
#         user = User.objects.filter(username=phone)
#         if not user:
#             number = User.objects.create(
#                     username=phone,
#                 )
#             sms_code = random.randint(1000, 9999)
#             number.phone = int(phone)
#             number.sms_code = sms_code
#             number.save()
#             if number:
#                 result = {
#                     'status': 1,
#                     'msg': 'Sms sended',
#                 }
#                 SendSmsApiWithEskiz(message="https://star-one.uz/ Tasdiqlash kodi " + str(sms_code), phone=phone).send()
#                 return Response(result, status=status.HTTP_200_OK)
#             else:
#                 return Response(status=status.HTTP_404_NOT_FOUND)
#         elif user.last().sms_status == False:
#             user.last().delete()
#             number = User.objects.create(
#                 username=phone,
#             )
#             sms_code = random.randint(1000, 9999)
#             number.phone = int(phone)
#             number.sms_code = sms_code
#             number.save()
#
#             if number:
#                 result = {
#                     'status': 1,
#                     'msg': 'Sms sended',
#                     'user': SerializerUser(number, many=False, context={"request": request}).data,
#                 }
#                 SendSmsApiWithEskiz(message="Tasdiqlash kodi " + str(sms_code), phone=phone).send()
#                 return Response(result, status=status.HTTP_200_OK)
#         else:
#             res = {
#                 'status': 0
#             }
#
#             return Response(res, status=status.HTTP_200_OK)
#
#     except KeyError:

        # return Response(status=status.HTTP_404_NOT_FOUND)
