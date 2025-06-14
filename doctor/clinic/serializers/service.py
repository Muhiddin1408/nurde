from rest_framework import serializers

from apps.clinic.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Service
        fields = '__all__'

    def get_category_name(self, obj):
        if obj.category:
            return obj.category.name
        return None
