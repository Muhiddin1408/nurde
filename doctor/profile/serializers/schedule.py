from rest_framework import serializers

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
