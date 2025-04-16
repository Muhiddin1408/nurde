import random
from datetime import timedelta, datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.auth.serializers.register import RegisterSerializer, PasswordSerializers
from api.utils.eskiz import SendSmsApiWithEskiz
from apps.users.models import User

class RegisterView(APIView):
    permission_classes = [AllowAny,]
    throttle_scope = "authentication"
    throttle_classes = [ScopedRateThrottle,]

    @swagger_auto_schema(
        tags=['authentication'],
        request_body=RegisterSerializer,
        responses={201: RegisterSerializer}
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        phone = request.data('phone')
        sms_code = random.randint(1000, 9999)
        user = User.objects.get(username=phone)
        user.sms_code = sms_code
        user.sms_code_time = datetime.now() + timedelta(minutes=2)
        SendSmsApiWithEskiz(message="https://star-one.uz/ Tasdiqlash kodi " + str(sms_code), phone=phone).send()
        return Response(status=status.HTTP_200_OK)

    @action(methods='POST', detail=False)
    def sms_conf(self, request, *args, **kwargs):
        try:
            sms_code = request.data['code']
            phone = request.data['phone']
            user = User.objects.get(username=phone)
            if user and user.sms_code == sms_code and user.sms_code_time <= datetime.now():
                return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods='POST', detail=False)
    def password_conf(self, request, *args, **kwargs):
        serializer = PasswordSerializers(request.data)
        serializer.save()
        return Response(status=status.HTTP_200_OK)





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
