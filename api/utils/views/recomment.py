from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from api.order.serializers.order import MyOrderSerializers
from apps.order.models import Order
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment(request):
    order = Order.objects.filter(status='inactive', recomment=False).last()
    if not order:
        return Response({'detail': ' '}, status=status.HTTP_404_NOT_FOUND)
    order.comment = True
    order.save()
    serializer = MyOrderSerializers(order, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)
