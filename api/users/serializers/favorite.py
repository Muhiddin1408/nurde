from rest_framework import serializers

from api.basic.serializers.specialist import SpecialistSerializers
from apps.utils.models.like import Like


class LikeSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ('id', 'doctor', 'created_at')

    def get_doctor(self, obj):
        return SpecialistSerializers(obj.doctor, context={'request': self.context['request']}).data
