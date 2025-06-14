from rest_framework import serializers

from apps.basic.models import Worker


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
        if obj.clinic.image:
            return request.build_absolute_uri(obj.clinic.image.url)
        return None

