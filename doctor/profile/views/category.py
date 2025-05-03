from rest_framework import generics, permissions

from apps.basic.models import Specialist
from doctor.profile.serializers.category import CategorySerializers


class CategoryListView(generics.RetrieveAPIView):
    queryset = Specialist.objects.all()
    serializer_class = CategorySerializers
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        specialist = Specialist.objects.get(user=user)
        return specialist