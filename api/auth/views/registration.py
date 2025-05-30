import random
import sys
from datetime import timedelta, datetime

from api.utils import google, apple
from core.settings import GOOGLE_CLIENT_ID
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import validate_email
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from packaging.utils import _
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.auth.serializers.register import RegisterSerializer, PasswordSerializers
from api.utils.eskiz import SendSmsApiWithEskiz
from api.utils.gmail_sms import send_sms, register_social_user, get_tokens_for_user
# from api.utils.gmail_sms import send_verification_email
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
        if phone.isdigit():
            user = User.objects.filter(username='u' + phone).last()
        else:
            user = User.objects.filter(username='u' + phone).last()
        if user is None:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            sms_code = random.randint(1000, 9999)
            user = User.objects.get(username='u' + phone)
            user.sms_code = sms_code
            user.save()
            if phone.isdigit():
                if is_all_digits(phone):
                    SendSmsApiWithEskiz(message="https://star-one.uz/ Tasdiqlash kodi " + str(sms_code),
                                        phone=int(phone)).send()
                # else:
                    # send_verification_email(phone, sms_code)
            else:
                send_sms(phone, f'Код подтверждения для приложения OVI '
                                f'Ваш код подтверждения для входа в приложение OVI: {sms_code}'
                                'Если у вас возникнут вопросы или потребуется помощь, пожалуйста, сообщите.')
            return Response({'status': False},status=status.HTTP_200_OK)
        elif not user.is_active:
            sms_code = random.randint(1000, 9999)
            user = User.objects.get(username='u' + phone)
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
        user = User.objects.filter(username='u' + phone).last()

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

        user = User.objects.get(username='u' + phone)

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

class LoginWithSocialAccountViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = None
    @swagger_auto_schema(
        methods=['post'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['auth_token'],
            properties={
                'auth_token': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
        operation_description='Enter token',
        responses={200: 'ok'}
    )
    @action(methods=['post'], detail=False, url_name='auth')
    def with_google(self, request, *args, **kwargs):
        try:
            auth_token = request.data['auth_token']
            status, user_data = google.Google.verify_auth_token(auth_token)
            if status:
                username = "u" + user_data['email']
                print(username)
                user = User.objects.filter(username=username).last()
                if user:
                    if user.is_active:
                        user = User.objects.get(username=username)
                    else:
                        User.objects.get(username='u' + user_data['email']).delete()
                        user = register_social_user(user_data['email'], user_data.get('given_name'),
                                                    user_data.get('family_name'), 'google')
                else:
                    user = register_social_user(user_data['email'], user_data.get('given_name'), user_data.get('family_name'), 'google')

                refresh, access = get_tokens_for_user(user)
                res = {
                    'refresh': refresh,
                    'access': access,
                    # 'user': user_data
                }

                return Response(res, 200)
            else:
                return Response(user_data, 400)
        except Exception as e:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            res = {'message': _(str(e) + ' - line -' + str(line))}
            return Response(res, status=400)

    @action(methods=['post'], detail=False, url_name='auth')
    def with_apple(self, request, *args, **kwargs):
        try:

            auth_token = request.data['auth_token']
            status, user_data = apple.AppleOAuth2().do_auth(auth_token)
            if status:
                username = 'u' + user_data
                print(username)
                user = User.objects.filter(username=username).exists()
                if user:
                    if user.is_active:
                        user = User.objects.get(username=username)
                    else:
                        User.objects.get(username=username).delete()
                        user = register_social_user(user_data," "," ",  'google')
                else:
                    user = register_social_user(user_data,  'google')

                refresh, access = get_tokens_for_user(user)
                res = {
                    'refresh': refresh,
                    'access': access,
                }

                return Response(res, 200)
            else:
                return Response(user_data, 400)

        except Exception as e:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            res = {'message': _(str(e) + ' - line -' + str(line))}
            return Response(res, status=400)
