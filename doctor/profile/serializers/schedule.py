from rest_framework import serializers, status
from rest_framework.response import Response

from apps.basic.models import Specialist
from apps.service.models.service import WorkTime
from apps.users.model import Weekday


class WeekdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Weekday
        fields = '__all__'


class MyScheduleSerializer(serializers.ModelSerializer):
    weekday_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WorkTime
        fields = ['id', 'weekday', 'weekday_name', 'date', 'finish']
        read_only_fields = ['id', 'weekday_name']

    def get_weekday_name(self, obj):
        return obj.weekday.name if obj.weekday else None

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            try:
                specialist = Specialist.objects.get(user=request.user)
            except Specialist.DoesNotExist:
                raise serializers.ValidationError({'user': 'Specialist not found'})
            validated_data['user'] = specialist
        else:
            raise serializers.ValidationError({'user': 'Invalid request context'})

        return super().create(validated_data)


class WorkTimeBulkSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        request = self.context.get('request')
        try:
            specialist = Specialist.objects.get(user=request.user)
        except Specialist.DoesNotExist:
            raise serializers.ValidationError({'user': 'Specialist not found'})

        instances = [WorkTime(user=specialist, **item) for item in validated_data]
        return WorkTime.objects.bulk_create(instances)


class WorkTimeSerializer(serializers.ModelSerializer):
    weekday = serializers.PrimaryKeyRelatedField(queryset=Weekday.objects.all())

    class Meta:
        model = WorkTime
        fields = ['weekday', 'date', 'finish']
        # list_serializer_class = WorkTimeBulkSerializer

    # def create(self, validated_data):


class WorkTimeBulkWrapperSerializer(serializers.Serializer):
    data = WorkTimeSerializer(many=True)

    def create(self, validated_data):
        request = self.context.get('request')
        WorkTime.objects.filter(user=request.user).delete()
        try:
            specialist = Specialist.objects.get(user=request.user)
        except Specialist.DoesNotExist:
            raise serializers.ValidationError({'user': 'Specialist not found'})
        created_worktimes = [
            WorkTime(
                user=specialist,
                weekday=item['weekday'],  # DRF allaqachon Weekday instance qilib beradi
                date=item.get('date'),
                finish=item.get('finish')
            )
            for item in validated_data['data']
        ]

        # bulk_create – tezroq
        WorkTime.objects.bulk_create(created_worktimes)

        # bulk_create qaytarmaydi id'lar bilan to‘ldirilgan obyektlar, shuning uchun qayta olib kelamiz
        return created_worktimes

    def to_representation(self, instance):
        return WorkTimeSerializer(instance, many=True, context=self.context).data

