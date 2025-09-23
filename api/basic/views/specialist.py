from datetime import datetime, time

from django.db.models import Avg, Count
from rest_framework import viewsets, permissions, status, generics, filters
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.basic.serializers.info import SpecialistInfoSerializer, CommentReadMoreSerializer, \
    CommentReadMoreCreateSerializer
from api.basic.serializers.service import ServiceSerializer
from api.basic.serializers.specialist import CategorySerializers, SpecialistSerializers, SpecialistByIdSerializers
from apps.basic.models import Specialist, CommentReadMore
from apps.service.models.service import Service
from apps.utils.models import Category


class SpecialistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class SmallPagesPagination(PageNumberPagination):
    page_size = 20


class SpecialistCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializers
    permission_classes = [permissions.AllowAny,]
    pagination_class = SmallPagesPagination

    def get_queryset(self):
        params = self.request.query_params
        category_ids = params.getlist('category')  # to'g'ridan to'g'ri list oladi
        sort_by = params.get('sort')
        type_ = params.get('type')

        queryset = Specialist.objects.all()

        if category_ids:
            queryset = queryset.filter(category__id__in=category_ids)

        if type_:
            if type_ == '1':
                queryset = queryset.filter(type='doctor')
            elif type_ == '2':
                queryset = queryset.filter(type='nurses')

        date = params.get('date')
        if date:
            dt = datetime.strptime(date, "%Y-%m-%d")

            queryset = queryset.filter(specialistinwork__weekday_name=str(dt.weekday()))

        time_period=params.get('time_period')
        if time_period:
            if time_period == 'morning':
                queryset = queryset.filter(specialistinwork__start__lte=time(12, 0))
            elif time_period == 'afternoon':
                queryset = queryset.filter(specialistinwork__start__lte=time(18, 0),
                                           specialistinwork__end__gte=time(12, 0))
            elif time_period == 'evening':
                queryset = queryset.filter(specialistinwork__start__gte=time(18, 0),)

        min_rating = params.get('min_rating')
        if min_rating:
            queryset = queryset.annotate(avg_ranking=Avg('commentreadmore__ranking')).filter(avg_ranking__gt=4)

        gender = params.get('gender')
        if gender:
            if gender == 'man':
                queryset = queryset.filter(gen='man')
            elif gender == 'woman':
                queryset = queryset.filter(gen='woman')


        if sort_by == '1':
            queryset = queryset
        elif sort_by == '2':
            queryset = queryset.annotate(avg_ranking=Avg('commentreadmore__ranking')).order_by('-avg_ranking')
        elif sort_by == '4':
            queryset = queryset.annotate(comment_count=Count('commentreadmore')).order_by('-comment_count')


        return queryset

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
        return Response(CommentReadMoreSerializer(comment, many=True, context={"request": request}).data)


class Comment(generics.CreateAPIView):
    queryset = CommentReadMore.objects.all()
    serializer_class = CommentReadMoreCreateSerializer
    permission_classes = [permissions.IsAuthenticated,]


class SpecialistByIdViewSet(APIView):
    permission_classes = [permissions.AllowAny,]

    def get(self, request, pk):
        try:
            specialist = Specialist.objects.get(pk=pk)
        except Specialist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SpecialistByIdSerializers(specialist, context={'request': request})
        return Response(serializer.data)






