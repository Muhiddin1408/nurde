from rest_framework import serializers

from apps.clinic.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ['clinic']

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
