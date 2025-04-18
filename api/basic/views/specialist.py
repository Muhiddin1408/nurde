from rest_framework import viewsets, permissions
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from api.basic.serializers.specialist import CategorySerializers, SpecialistSerializers
from apps.basic.models import Specialist
from apps.utils.models import Category


class SpecialistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    search_fields = ['name']



class SpecialistCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializers
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        category_ids = self.request.query_params.get('category')

        if category_ids:
            category = Category.objects.get(pk=category_ids)
            queryset = Specialist.objects.filter(category=category)



            return queryset
        return Specialist.objects.all()




