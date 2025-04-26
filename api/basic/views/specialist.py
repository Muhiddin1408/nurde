from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.basic.serializers.info import SpecialistInfoSerializer, CommentReadMoreSerializer
from api.basic.serializers.service import ServiceSerializer
from api.basic.serializers.specialist import CategorySerializers, SpecialistSerializers, SpecialistByIdSerializers
from apps.basic.models import Specialist, CommentReadMore
from apps.service.models.service import Service
from apps.utils.models import Category


class SpecialistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    search_fields = ['name']


class SmallPagesPagination(PageNumberPagination):
    page_size = 20


class SpecialistCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializers
    permission_classes = [permissions.AllowAny]
    pagination_class = SmallPagesPagination

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


class SpecialistByIdViewSet(APIView):
    def get(self, request, pk):
        try:
            specialist = Specialist.objects.get(pk=pk)
        except Specialist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SpecialistByIdSerializers(specialist, context={'request': request})
        return Response(serializer.data)






