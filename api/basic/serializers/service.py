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
        return obj.category.name
