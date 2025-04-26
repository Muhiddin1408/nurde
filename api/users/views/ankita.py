from rest_framework import viewsets, permissions

from api.basic.views.specialist import SmallPagesPagination
from api.users.serializers.ankita import AnkitaSerializer, RelativeSerializer
from apps.users.model import Ankita, Patient, Relative


class RelativeView(viewsets.ReadOnlyModelViewSet):
    queryset = Relative.objects.all()
    serializer_class = RelativeSerializer
    permission_classes = [permissions.IsAuthenticated]


class AnkitaView(viewsets.ModelViewSet):
    queryset = Ankita.objects.all()
    serializer_class = AnkitaSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SmallPagesPagination

    def get_queryset(self):
        user = self.request.user
        return Ankita.objects.filter(user=Patient.objects.filter(user=user).first())