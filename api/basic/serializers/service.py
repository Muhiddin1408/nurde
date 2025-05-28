from rest_framework import serializers

from apps.basic.models import Specialist
from apps.service.models.service import Service
from apps.utils.models import Category


class ServiceSerializers(serializers.Serializer):

    class Meta:
        model = Category
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField(read_only=True)  # faqat list uchun

    class Meta:
        model = Service
        fields = ['id', 'category', 'price', 'preparation', 'description', 'category_name', 'status']
        read_only_fields = ['id', 'category_name']

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

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
        validated_data['status'] = 'process'

        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['status'] = 'process'
        return super().update(instance, validated_data)


class ServiceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'id', 'category', 'price',
            'preparation', 'description',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def update(self, instance, validated_data):
        validated_data.pop('user', None)
        validated_data['status'] = 'process'
        return super().update(instance, validated_data)

