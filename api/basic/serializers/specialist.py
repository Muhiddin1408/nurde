
from rest_framework import serializers
from datetime import datetime
from apps.basic.models import Specialist
from apps.service.models.booked import Booked
from apps.service.models.service import WorkTime
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

    class Meta:
        model = Specialist
        fields = (
            'id', 'last_name', 'first_name', 'middle_name',
            'experience', 'category', 'type', 'type_service', 'photo', 'work_time'
        )

    def get_last_name(self, obj):
        print(obj)
        return obj.user.last_name

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_middle_name(self, obj):
        return obj.user.middle_name

    def get_category(self, obj):
        return

    def get_work_time(self, obj):
        now = datetime.now()
        print(self.context['request'])
        request = self.context['request']
        date = request.GET.get('date')
        time = request.GET.get('time')
        weekday = now.weekday()
        work = WorkTime.objects.filter(user=obj.id, weekday__name=weekday)
        if date:
            work = WorkTime.objects.filter(user=obj.id, weekday__name=weekday, date__date=date)
        if time == 'before':
            now = datetime.now()
            twelve_pm_today = datetime.combine(now.date(), time(12, 0))
            work = work(user=obj.id, date__hour__lte=12)
        elif time == 'mid':
            work = work(user=obj.id, date__hour__gt=12, date__hour__lte=18)
        elif time == 'after':
            work = work(user=obj.id, date__hour__gt=18)
        else:
            WorkTime.objects.filter(user=obj.id, weekday__name=weekday)





        booked_ids = Booked.objects.filter(
            worktime__in=work
        ).values_list('worktime_id', flat=True)
        free_worktimes = work.exclude(id__in=booked_ids)
        return WorkTimeSerializer(free_worktimes, many=True).data

