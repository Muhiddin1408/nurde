from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from api.basic.serializers.info import SpecialistInfoSerializer, CommentReadMoreSerializer
from api.basic.serializers.service import ServiceSerializer
from api.basic.serializers.specialist import CategorySerializers, SpecialistSerializers
from apps.basic.models import Specialist, CommentReadMore
from apps.service.models.service import Service
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
        sort_by = self.request.query_params.get('sort')
        if category_ids:
            queryset = Specialist.objects.filter(category__id__in=category_ids)
            if sort_by == 'ranking':
                queryset = Specialist.objects.filter(category__id__in=category_ids)

            return queryset
        return Specialist.objects.all()

    @action(detail=True, methods=['GET'])
    def info(self, request, pk=None):
        query = Specialist.objects.get(id=pk)
        serializer = SpecialistInfoSerializer(query)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def services(self, request, pk=None):
        query = Service.objects.filter(user_id=pk)
        serializer = ServiceSerializer(query, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def comment(self, request, pk=None):
        query = Specialist.objects.get(id=pk)
        comment = CommentReadMore.objects.filter(read_more=query)
        return Response(CommentReadMoreSerializer(comment, many=True).data)







