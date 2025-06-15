# from payment.views.view import PaymeWebHookAPIView
#
#
# class PaymeCallBackAPIView(PaymeWebHookAPIView):
#     def handle_created_payment(self, params, result, *args, **kwargs):
#         """
#         Handle the successful payment. You can override this method
#         """
#         print(f"Transaction created for this params: {params} and cr_result: {result}")
#
#     def handle_successfully_payment(self, params, result, *args, **kwargs):
#         """
#         Handle the successful payment. You can override this method
#         """
#         print(f"Transaction successfully performed for this params: {params} and performed_result: {result}")
#
#     def handle_cancelled_payment(self, params, result, *args, **kwargs):
#         """
#         Handle the cancelled payment. You can override this method
#         """
#         print(f"Transaction cancelled for this params: {params} and cancelled_result: {result}")

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.order.models import Order

# from .models import Order
# from .serializers import OrderSerializer
# from .utils.payme import generate_payme_link

MERCHANT_ID = "6830068ddfc9ac0473674de8"  # o'zgaruvchi sifatida tashqariga chiqarib qo'ying4
# utils/payme.py
import base64

def generate_payme_link(order_id, amount, merchant_id):
    """
    amount so'mda (masalan: 5000)
    Payme uchun tiyin kerak => amount * 100
    """
    amount_in_tiyin = amount * 100
    payload = f"{merchant_id}:{order_id}".encode('utf-8')
    encoded_id = base64.b64encode(payload).decode('utf-8')

    return f"https://checkout.paycom.uz/{encoded_id}?amount={amount_in_tiyin}&account[order_id]={order_id}"


class PaymeInitAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        if not amount:
            return Response({'error': 'Amount is required'}, status=400)

        order = Order.objects.create(user=request.user, amount=amount)
        payme_link = generate_payme_link(order.id, order.amount, MERCHANT_ID)

        return Response({
            "order_id": order.id,
            "payme_url": payme_link
        })

# views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def payme_callback(request):
    data = json.loads(request.body)

    method = data.get("method")
    params = data.get("params", {})
    order_id = params.get("account", {}).get("order_id")

    if not order_id:
        return JsonResponse({"error": "order_id not found"}, status=400)

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found"}, status=404)

    if method == "CheckPerformTransaction":
        return JsonResponse({
            "result": {
                "allow": True
            }
        })

    elif method == "CreateTransaction":
        order.payme_transaction_id = params.get("id")
        order.save()
        return JsonResponse({
            "result": {
                "create_time": int(order.created_at.timestamp() * 1000),
                "transaction": params.get("id"),
                "state": 1
            }
        })

    elif method == "PerformTransaction":
        order.is_paid = True
        order.save()
        return JsonResponse({
            "result": {
                "transaction": order.payme_transaction_id,
                "perform_time": int(order.created_at.timestamp() * 1000),
                "state": 2
            }
        })

    elif method == "CancelTransaction":
        order.is_paid = False
        order.save()
        return JsonResponse({
            "result": {
                "transaction": order.payme_transaction_id,
                "cancel_time": int(order.created_at.timestamp() * 1000),
                "state": -1
            }
        })

    return JsonResponse({"error": "Unknown method"}, status=400)

