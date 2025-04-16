from rest_framework import viewsets

from api.basic.serializers.specialist import CategorySerializers, SpecialistSerializers
from apps.basic.models import Specialist
from apps.utils.models import Category


class SpecialistViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    search_fields = ['name']


class SpecialistCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializers

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return SpecialistSerializers(queryset, many=True).data




