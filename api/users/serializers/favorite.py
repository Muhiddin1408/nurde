from rest_framework import serializers

from api.basic.serializers.specialist import SpecialistSerializers
from api.clinic.serializers.clinic import ClinicSerializers
from apps.users.model import Patient
from apps.utils.models.like import Like


class LikeSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()
    clinic = serializers.SerializerMethodField()

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

    def get_clinic(self, obj):
        if obj.clinic:
            return ClinicSerializers(obj.clinic, context={'request': self.context.get('request')}).data
        return None

    def create(self, validated_data):
        request = self.context['request']
        specialist_id = request.data.get('user')  # user id keladi
        clinic_id = request.data.get('clinic')    # clinic id keladi

        like, created = Like.objects.get_or_create(
            costumer=Patient.objects.filter(user=request.user).last(),
            user_id=specialist_id,
            clinic_id=clinic_id
        )
        return like
