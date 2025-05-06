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
        fields = ['id', 'weekday', 'weekday_name', 'date']
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
    class Meta:
        model = WorkTime
        fields = ['weekday', 'date', 'finish']
        # list_serializer_class = WorkTimeBulkSerializer

    # def create(self, validated_data):


class WorkTimeBulkWrapperSerializer(serializers.Serializer):
    data = serializers.ListField()

    def create(self, validated_data):
        request = self.context.get('request')
        try:
            specialist = Specialist.objects.get(user=request.user)
        except Specialist.DoesNotExist:
            raise serializers.ValidationError({'user': 'Specialist not found'})

        # validated_data['data'] bu ro'yxat
        for item in validated_data['data']:
            WorkTime.objects.create(
                user=specialist,
                weekday=Weekday.objects.get(id=item['weekday']),
                date=item.get('date'),
                finish=item.get('finish')
            )

        return Response(status=status.HTTP_201_CREATED)

    def to_representation(self, instance):
        return WorkTimeSerializer(instance, many=True).data

