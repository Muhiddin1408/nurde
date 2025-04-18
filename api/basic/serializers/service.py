from rest_framework import serializers

from apps.clinic.models import Service
from apps.utils.models import Category


class ServiceSerializers(serializers.Serializer):

    class Meta:
        model = Category
        fields = '__all__'
