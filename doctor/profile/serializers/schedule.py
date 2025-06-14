from rest_framework import serializers, status
from rest_framework.response import Response

from apps.basic.models import Specialist, Worker
from apps.service.models.service import WorkTime
from apps.users.model import Weekday, Image


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
        WorkTime.objects.filter(user__user=request.user).delete()
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

        return created_worktimes

    def to_representation(self, instance):
        return WorkTimeSerializer(instance, many=True, context=self.context).data


class WorkTimeBulkClinicSerializer(serializers.Serializer):
    data = WorkTimeSerializer(many=True, required=True)
    phone = serializers.IntegerField(write_only=True, required=False)
    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)
    address = serializers.CharField(write_only=True, required=False)
    image_id = serializers.IntegerField(write_only=True, required=False)
    description = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):
        request = self.context.get('request')
        WorkTime.objects.filter(user__user=request.user).delete()
        try:
            clinic = request.user.specialist.adminclinic.clinic

        except Specialist.DoesNotExist:
            raise serializers.ValidationError({'user': 'Specialist not found'})
        worktime_data = validated_data.pop('data')
        result = []
        for item in worktime_data:
            weekday = item['weekday']
            date = item.get('date')
            finish = item.get('finish')

            # clinic va weekday bo‘yicha tekshirib update yoki create qilish
            obj, _ = WorkTime.objects.update_or_create(
                clinic=clinic,
                weekday=weekday,
                defaults={
                    'date': date,
                    'finish': finish,
                    'clinic': clinic
                }
            )
            result.append(obj)
        fields_to_update = ['phone', 'latitude', 'longitude', 'address', 'description']
        updated = False

        for field in fields_to_update:
            if field in validated_data:
                setattr(clinic, field, validated_data[field])
                updated = True

        if updated:
            clinic.save()
        image_id = validated_data.get('image_id')
        if image_id:
            try:
                image = Image.objects.get(id=image_id)
                image.clinic = specialist
                image.save()
            except Image.DoesNotExist:
                raise serializers.ValidationError({'image_id': 'Image not found'})

        return created_worktimes


class WorkTimeClinicSerializer(serializers.Serializer):
    data = WorkTimeSerializer(many=True, required=True)
    status = serializers.CharField(write_only=True, required=False)
    specialist = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        request = self.context.get('request')
        WorkTime.objects.filter(user__user=request.user).delete()
        try:
            clinic = request.user.specialist.adminclinic.clinic

        except Specialist.DoesNotExist:
            raise serializers.ValidationError({'user': 'Specialist not found'})
        created_worktimes = [
            WorkTime(
                user_id=validated_data['specialist'],
                weekday=item['weekday'],
                date=item.get('date'),
                finish=item.get('finish'),
                clinic=clinic

            )
            for item in validated_data['data']
        ]
        if validated_data['status']:
            Worker.objects.filter(specialist_id=validated_data['specialist']).update(status=validated_data['status'])

        WorkTime.objects.bulk_create(created_worktimes)
        return created_worktimes

    def to_representation(self, instance):
        return WorkTimeSerializer(instance, many=True, context=self.context).data

