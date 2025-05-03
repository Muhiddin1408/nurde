from rest_framework import serializers

from apps.service.models.service import Service
from apps.utils.models import Category


class ServiceSerializers(serializers.Serializer):

    class Meta:
        model = Category
        fields = '__all__'


class ServiceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    description = serializers.CharField(read_only=True)
    category = serializers.SerializerMethodField()
    preparation = serializers.CharField(read_only=True)
    time = serializers.IntegerField(read_only=True)

    class Meta:
        model = Service
        fields = '__all__'

    def get_category(self, obj):
        if obj.category:
            return obj.category.name
        return None


class ServiceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'id', 'category', 'price',
            'preparation', 'time', 'description',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def update(self, instance, validated_data):
        validated_data.pop('user', None)
        return super().update(instance, validated_data)

