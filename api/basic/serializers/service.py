from rest_framework import serializers

from apps.clinic.models import Service


class ServiceSerializers(serializers.Serializer):

    class Meta:
        model = Service
        fields = ('id', 'name', 'type', 'image')