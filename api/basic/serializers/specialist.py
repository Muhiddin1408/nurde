from django.db.models import Sum
from rest_framework import serializers
from datetime import datetime, time as time_obj

from api.basic.serializers.in_work import InWorkSerializer
from api.basic.serializers.service import ServiceSerializer
from apps.basic.models import Specialist, CommentReadMore
from apps.basic.models.in_work import InWork
from apps.service.models.booked import Booked
from apps.service.models.service import WorkTime, Service
from apps.utils.models import Category


class WorkTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkTime
        fields = '__all__'


class CategorySerializers(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    icon = serializers.FileField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'icon')

    def get_icon(self, obj):
        print(obj)
        return obj.icon.url


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class SpecialistSerializers(serializers.ModelSerializer):
    last_name = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    middle_name = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    work_time = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    ranking = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    in_work = serializers.SerializerMethodField()

    class Meta:
        model = Specialist
        fields = (
            'id', 'last_name', 'first_name', 'middle_name', 'service', 'price',
            'experience', 'category', 'type', 'type_service', 'photo', 'work_time', 'avatar', 'comment',
            'ranking', 'in_work'
        )

    def get_avatar(self, obj):
        if obj.photo:
            return obj.photo.url
        return None

    def get_last_name(self, obj):
        print(obj)
        return obj.user.last_name

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_middle_name(self, obj):
        return obj.user.middle_name

    def get_category(self, obj):
        return CategorySerializer(obj.category, many=True).data

    def get_work_time(self, obj):
        request = self.context['request']
        now = datetime.now()
        now_time = now.time()
        today_weekday = now.weekday()
        query_date = request.GET.get('date')
        query_time = request.GET.get('time')
        work_qs = WorkTime.objects.filter(user=obj.id)

        if query_date:
            work_qs = work_qs.filter(date__date=query_date)
        else:
            work_qs = work_qs.filter(weekday__name=today_weekday)
        if query_time == 'before':
            work_qs = work_qs.filter(date__lt=time_obj(12, 0))
        elif query_time == 'mid':
            work_qs = work_qs.filter(date__gte=time_obj(12, 0), date__lt=time_obj(18, 0))
        elif query_time == 'after':
            work_qs = work_qs.filter(date__gte=time_obj(18, 0))
        booked_ids = Booked.objects.filter(worktime__in=work_qs).values_list('worktime_id', flat=True)
        available_times = work_qs.exclude(id__in=booked_ids)
        final_times = available_times.filter(date__gt=now_time)
        return WorkTimeSerializer(final_times, many=True).data

    def get_ranking(self, obj):
        total_ranking = CommentReadMore.objects.filter(read_more=obj).aggregate(Sum('ranking'))['ranking__sum'] or 0
        len = CommentReadMore.objects.filter(read_more=obj).count() or 1
        return total_ranking/len

    def get_comment(self, obj):
        comment = CommentReadMore.objects.filter(read_more=obj.id).count()
        return comment

    def get_price(self, obj):
        service = Service.objects.filter(user=obj.id).order_by('price').first()
        return service.price

    def get_service(self, obj):
        service = Service.objects.filter(user=obj.id)
        return ServiceSerializer(service, many=True).data

    def get_in_work(self, obj):
        in_work = InWork.objects.filter(specialist=obj)
        return InWorkSerializer(in_work, many=True).data






