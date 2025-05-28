from django.http import JsonResponse


def check_method(data):
    method = data.get('method')
    params = data.get('params', {})
    request_id = data.get('id', 0)

    if method == 'CheckPerformTransaction':
        return check_perform(params, request_id)
    else:
        return JsonResponse({
            'id': request_id,
            'error': {'code': -32601, 'message': 'Method not found'}
        })


def check_perform(params, request_id):
    account = params.get('account', {})
    order_id = account.get('order_id')
    username = account.get('username')
    amount = params.get('amount')

    # Simulyatsiya: bu yerda DBdan tekshirish bo'lishi kerak
    if order_id == "ORD-20250528-0012" and username == "john_doe":
        return JsonResponse({
            'id': request_id,
            'result': {
                'allow': True,
                'reason': None,
                'info': {
                    'order_id': order_id,
                    'username': username,
                    'amount': amount,
                    'service': 'Konsultatsiya'
                }
            }
        })
    else:
        return JsonResponse({
            'id': request_id,
            'error': {
                'code': -31050,
                'message': {
                    'uz': 'Buyurtma yoki foydalanuvchi topilmadi',
                    'ru': 'Заказ или пользователь не найден'
                }
            }
        })
