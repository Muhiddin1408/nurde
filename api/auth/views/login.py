from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User


@api_view(['POST'])
@permission_classes([AllowAny, ])
def login(request):
    try:
        phone = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=phone).first()
        if user and user.check_password(password):
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

