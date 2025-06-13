from django.conf import settings

from apps.clinic.models import Symptom

import os
import pandas as pd
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.utils.models import Category


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def symbtom(request):
    file_path = os.path.join(settings.BASE_DIR, 'static', 'aaaaa.xlsx')  # Fayl nomini moslashtiring
    if not os.path.exists(file_path):
        return Response({"error": "Fayl topilmadi: mmm.xlsx"}, status=400)

    df = pd.read_excel(file_path)

    for index, row in df.iterrows():
        name = f'{row[1]}'  # Ustun indekslarini tekshiring
        Category.objects.create(name=name,)

    return Response({"message": "Ma'lumotlar muvaffaqiyatli saqlandi"})