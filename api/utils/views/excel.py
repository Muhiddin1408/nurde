
from apps.clinic.models import Symptom

import os
import pandas as pd
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def symbtom(request):
    file_path = 'mmm.xlsx'  # Fayl nomini moslashtiring
    if not os.path.exists(file_path):
        return Response({"error": "Fayl topilmadi: mmm.xlsx"}, status=400)

    df = pd.read_excel(file_path)

    for index, row in df.iterrows():
        name = f'{row[1]} | {row[2]}'  # Ustun indekslarini tekshiring
        Symptom.objects.create(name=name, type='diagnoses')

    return Response({"message": "Ma'lumotlar muvaffaqiyatli saqlandi"})