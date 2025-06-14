from rest_framework import serializers

from apps.basic.models import Worker
from apps.users.model import Image


class WorkerDoctorSerializer(serializers.Serializer):
    clinic = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    class Meta:
        model = Worker
        fields = ('id', 'clinic', 'status', 'image')

    def get_clinic(self, obj):
        return obj.clinic.name

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.clinic:
            image = Image.objects.filter(clinic=obj.clinic).last()
            return request.build_absolute_uri(image.image.url)
        return None

