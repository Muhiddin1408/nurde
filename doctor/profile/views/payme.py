import base64

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json

from apps.basic.models import Balance, Payment
from apps.users.models import User
from payment.views.payme import MERCHANT_ID


def generate_doctor_link(username):
    """
    amount so'mda (masalan: 5000)
    Payme uchun tiyin kerak => amount * 100
    """
    # amount_in_tiyin = amount * 100
    payload = f"{MERCHANT_ID}:{username}".encode('utf-8')
    encoded_id = base64.b64encode(payload).decode('utf-8')

    return f"https://checkout.paycom.uz/{encoded_id}?order_id={username}"


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment(request):
    """
    Foydalanuvchining username asosida to'lov havolasini (link) yaratadi va qaytaradi.
    """
    user = request.user
    username = user.username
    link = generate_doctor_link(username)
    return Response({'link': link})

@csrf_exempt
def payme_callback_doctor(request):
    data = json.loads(request.body)

    method = data.get("method")
    params = data.get("params", {})
    amount = data.get("amount")
    username = params.get("account", {}).get("username")

    # if not order_id:
    #     return JsonResponse({"error": "order_id not found"}, status=400)
    #
    # try:
    #     order = Order.objects.get(id=order_id)
    # except Order.DoesNotExist:
    #     return JsonResponse({"error": "Order not found"}, status=404)
    user = User.objects.get(username=username)

    if method == "CheckPerformTransaction":
        balance = Balance.objects.get(user=user)
        if balance.excit():
            balance.amount += amount
            balance.save()
        else:
            balance = Balance(user=user, amount=amount)

        Payment.objects.create(user=user, amount=amount, status='doctor')

        return JsonResponse({
            "result": {
                "allow": True,
                "username": username,
                "amount": amount,
                "status": 'doctor',
            }
        })

    elif method == "CreateTransaction":
        # order.payme_transaction_id = params.get("id")
        # order.save()
        return JsonResponse({
            "result": {
                # "create_time": int(order.created_at.timestamp() * 1000),
                "transaction": params.get("id"),
                "state": 1
            }
        })

    elif method == "PerformTransaction":
        # order.is_paid = True
        # order.save()
        return JsonResponse({
            "result": {
                # "transaction": order.payme_transaction_id,
                # "perform_time": int(order.created_at.timestamp() * 1000),
                "state": 2
            }
        })

    elif method == "CancelTransaction":
        # order.is_paid = False
        # order.save()
        return JsonResponse({
            "result": {
                # "transaction": order.payme_transaction_id,
                # "cancel_time": int(order.created_at.timestamp() * 1000),
                "state": -1
            }
        })

    return JsonResponse({"error": "Unknown method"}, status=400)


