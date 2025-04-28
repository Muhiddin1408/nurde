from rest_framework import serializers

from api.basic.serializers.specialist import SpecialistSerializers
from apps.users.model import Patient
from apps.utils.models.like import Like


class LikeSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ('id', 'doctor', 'created_at', 'user', 'clinic')

    def get_doctor(self, obj):
        if obj.user:
            return SpecialistSerializers(
                obj.user,
                context={'request': self.context.get('request')}
            ).data
        return None

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['costumer'] = Patient.objects.filter(user=request.user).last()
        return super().create(validated_data)
