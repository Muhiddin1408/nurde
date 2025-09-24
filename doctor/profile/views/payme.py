import base64
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json

from apps.basic.models import Balance, Payment
from apps.basic.models.payme import Payme
from apps.users.models import User
from payment.views.payme import MERCHANT_ID


def generate_doctor_link(username):
    """
    amount so'mda (masalan: 5000)
    Payme uchun tiyin kerak => amount * 100
    """
    # amount_in_tiyin = amount * 100
    payload = f"m={MERCHANT_ID};as.order_id={username};a=100;l=uz".encode()
    encoded_id = base64.b64encode(payload).decode()

    return f"https://checkout.paycom.uz/{encoded_id}"


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment(request):
    """
    Foydalanuvchining username asosida to'lov havolasini (link) yaratadi va qaytaradi.
    """
    user = request.user
    username = user.username
    doctor = user.specialist
    print(doctor, 'ssssssssssssssssssssssssssssssssssssss')
    if doctor:
        link = generate_doctor_link(username)
        return Response({'link': link})
    return JsonResponse({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
def payme_callback_doctor(request):
    data = json.loads(request.body)

    method = data.get("method")
    params = data.get("params", {})
    # amount = data.get("amount")
    username = params.get("account", {}).get("username")

    # if not order_id:
    #     return JsonResponse({"error": "order_id not found"}, status=400)
    #
    # try:
    #     order = Order.objects.get(id=order_id)
    # except Order.DoesNotExist:


    if method == "CheckPerformTransaction":
        if not username:
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
        user = User.objects.filter(username=username).last()
        if not user:
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
        balance = Balance.objects.filter(user=user).last()
        amount = params.get("amount")
        if balance:
            balance.balance += amount
            balance.save()
        else:
            Balance.objects.create(user=user, balance=amount)

        payment = Payment.objects.create(user=user, amount=amount, status='doctor')

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
        Payme.objects.create(id_name=params.get("id"), amount=params.get("amount"), method="CreateTransaction", crated_at=params.get("time"), state=1)
        return JsonResponse({
            "result": {
                "create_time": params.get('time'),
                "transaction": params.get("id"),
                "state": 1,
                'username': username,
                "amount": params.get("amount"),
            }
        })

    elif method == "PerformTransaction":
        payme = Payme.objects.filter(id_name=params.get("id")).last()
        if payme:
            if not payme.perform_time:
                payme.perform_time = int(datetime.now().timestamp() * 1000)
                payme.save()
        else:
            payme = Payme.objects.create(id_name=params.get("id"), payment_time=int(datetime.now().timestamp() * 1000))
        payme.state = 2
        payme.save()
        return JsonResponse({
            "result": {
                "transaction": params.get("id"),
                "perform_time": payme.perform_time,
                "state": 2
            }
        })

    elif method == "CancelTransaction":
        # order.is_paid = False
        # order.save()
        payme = Payme.objects.filter(id_name=params.get("id")).last()
        if not payme.cancel_at:
            payme.cancel_at = int(datetime.now().timestamp() * 1000)
            payme.save()
        payme.state = -2
        payme.reason = 5
        payme.save()
        return JsonResponse({
            "result": {
                "transaction": params.get("id"),
                "cancel_time": payme.cancel_at,
                "state": -2
            }
        })
    elif method == "CheckTransaction":
        # order.is_paid = False
        # order.save()
        get = Payme.objects.filter(id_name=params.get("id")).last()
        return JsonResponse({
            "result": {
                "transaction": params.get("id"),
                "cancel_time": get.cancel_at or 0,
                "create_time": get.crated_at or 0,
                "reason": get.reason,
                "perform_time": get.perform_time or 0,
                "state": get.state
            },
            "id": data.get("id"),
            "jsonrpc": data.get("jsonrpc"),
        })

    return JsonResponse({"error": "Unknown method"}, status=400)


