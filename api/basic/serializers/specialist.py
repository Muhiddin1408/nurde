
from rest_framework import serializers
from datetime import datetime
from apps.basic.models import Specialist
from apps.service.models.booked import Booked
from apps.service.models.service import WorkTime
from apps.utils.models import Category


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


class SpecialistSerializers(serializers.Serializer):
    last_name = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    middle_name = serializers.CharField(read_only=True)
    category = CategorySerializers(read_only=True)
    ranking = serializers.IntegerField(read_only=True)
    comment = serializers.IntegerField()

    class Meta:
        model = Specialist
        fields = ('id', 'last_name', 'first_name', 'middle_name', 'experience', 'category', 'ranking', 'comment',
                  'work_time')
    def get_work_time(self, obj):
        now = datetime.now()
        date = self.context['date']
        time = self.context['time']
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
        return free_worktimes

