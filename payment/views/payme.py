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
from datetime import datetime

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.basic.models.payme import Payme
from apps.order.models import Order

# from .models import Order
# from .serializers import OrderSerializer
# from .utils.payme import generate_payme_link

MERCHANT_ID = "6830068ddfc9ac0473674de8"  # o'zgaruvchi sifatida tashqariga chiqarib qo'ying4
# utils/payme.py
import base64

def generate_payme_link(order_id, amount):
    """
    amount so'mda (masalan: 5000)
    Payme uchun tiyin kerak => amount * 100
    """
    amount_in_tiyin = amount * 100
    payload = f"{MERCHANT_ID}:{order_id}".encode('utf-8')
    encoded_id = base64.b64encode(payload).decode('utf-8')

    return f"https://checkout.paycom.uz/{encoded_id}?amount={amount_in_tiyin}&order_id={order_id}"


class PaymeInitAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        if not amount:
            return Response({'error': 'Amount is required'}, status=400)

        order = Order.objects.create(user=request.user, amount=amount)
        payme_link = generate_payme_link(order.id, order.amount)

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
        return JsonResponse({
            "error": {
                "message": {
                    'en': "User not found",
                    'ru': "Такой пользователь не найден",
                    'uz': "Bunaqa user topilmadi"
                },
                "code": -32504,
            },
            "id": data.get("id"),
            "jsonrpc": data.get("jsonrpc"),
        })

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({
            "error": {
                "message": {
                    'en': "User not found",
                    'ru': "Такой пользователь не найден",
                    'uz': "Bunaqa user topilmadi"
                },
                "code": -31050,
            },
            "id": data.get("id"),
            "jsonrpc": data.get("jsonrpc"),
        })

    if int(order.price) != int(params.get("amount", 0)):
        return JsonResponse({
            "error": {
                "message": {
                    'en': "User not found",
                    'ru': "Такой пользователь не найден",
                    'uz': "Bunaqa user topilmadi"
                },
                "code": -31001,
            },
            "id": data.get("id"),
            "jsonrpc": data.get("jsonrpc"),
        })

    if method == "CheckPerformTransaction":
        return JsonResponse({
            "result": {
                "allow": True
            }
        })


    elif method == "CreateTransaction":

        # order.payme_transaction_id = params.get("id")

        # order.save()

        Payme.objects.create(id_name=params.get("id"), amount=params.get("amount"), method="CreateTransaction",
                             crated_at=params.get("time"))

        return JsonResponse({

            "result": {

                "create_time": params.get('time'),

                "transaction": params.get("id"),

                "state": 1,


                "amount": params.get("amount"),

            }

        })

    elif method == "PerformTransaction":
        payme = Payme.objects.filter(id_name=params.get("id")).first()
        payme.perform_time = int(datetime.now().timestamp() * 1000)
        payme.save()
        return JsonResponse({
            "result": {
                "transaction": params.get("id"),
                "perform_time": int(datetime.now().timestamp() * 1000),
                "state": 2
            }
        })

    elif method == "CancelTransaction":
        payme = Payme.objects.filter(id_name=params.get("id")).last()
        payme.cancel_at = int(datetime.now().timestamp() * 1000)
        payme.save()
        return JsonResponse({
            "result": {
                "transaction": params.get("id"),
                "cancel_time": int(datetime.now().timestamp() * 1000),
                "state": -1
            }
        })

    elif method == "CheckTransaction":
        # order.is_paid = False
        # order.save()
        get = Payme.objects.filter(id_name=params.get("id")).last()
        return JsonResponse({
            "result": {
                "transaction": params.get("id"),
                "cancel_time": 0,
                "create_time": get.crated_at,
                "reason": None,
                "perform_time": get.perform_time,
                "state": 1
            },
            "id": data.get("id"),
            "jsonrpc": data.get("jsonrpc"),
        })
    return JsonResponse({"error": "Unknown method"}, status=400)

