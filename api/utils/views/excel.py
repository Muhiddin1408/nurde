import pandas as pd
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.clinic.models import Symptom


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def symbtom(request):
    file_path = 'mmm.xlsx'  # Fayl nomini o'zingizga moslashtiring
    df = pd.read_excel(file_path)

    # Ma'lumotlarni ko'rish
    for index, row in df.iterrows():
        name = f'{row[1]} | {row[2]}'
        Symptom.objects.create(name=name, type='diagnoses')

    return Response()