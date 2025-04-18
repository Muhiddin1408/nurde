from datetime import timedelta

from django.template.defaultfilters import date

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.service.models.booked import Booked
from apps.service.models.service import WorkTime


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_list(request):
    today = date.today()
    data = {
        'today': f'{today.strftime('%A'), today, count(today)}',
        'tomorrow': f'{(today + timedelta(days=1)).strftime('%A'), today + timedelta(days=1), count(today+ timedelta(days=1))}',
        'after_tomorrow': f'{(today + timedelta(days=2)).strftime('%A'), today + timedelta(days=2), count(today+ timedelta(days=2))}',
    }
    return Response(data)


def count(date):
    query = WorkTime.objects.filter(date__date=date)
    booked_ids = Booked.objects.filter(
        worktime__in=query
    ).values_list('worktime_id', flat=True)
    free_worktimes = query.exclude(id__in=booked_ids)
    return len(free_worktimes)

