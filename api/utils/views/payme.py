import json
import base64
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from api.utils.payme import check_method


@csrf_exempt
def payme_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': {'code': -32600, 'message': 'Invalid request'}}, status=400)

    # Auth tekshirish
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Basic '):
        return JsonResponse({'error': {'code': -32504, 'message': 'Authorization required'}}, status=401)

    encoded = auth_header.split(' ')[1]
    decoded = base64.b64decode(encoded).decode()
    if not decoded.endswith(settings.PAYME_SECRET_KEY):
        return JsonResponse({'error': {'code': -32504, 'message': 'Invalid merchant key'}}, status=401)

    # JSON body
    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({'error': {'code': -32700, 'message': 'Parse error'}}, status=400)

    return check_method(data)