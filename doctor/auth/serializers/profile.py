from rest_framework import serializers

from apps.basic.models import Specialist, AdminClinic


class ProfileSerializer(serializers.Serializer):
    photo = serializers.ImageField()
    last_name = serializers.CharField(source='user.last_name')
    first_name = serializers.CharField(source='user.first_name')
    middle_name = serializers.CharField(source='user.middle_name')
    phone_number = serializers.CharField(source='user.phone_number')
    email = serializers.CharField(source='user.email')
    pinfl = serializers.CharField()
    description = serializers.CharField()
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username[1:] if obj.user.username else ''

    class Meta:
        model = Specialist
        fields = '__all__'


class AdminClinicSerializers(serializers.ModelSerializer):
    class Meta:
        model = AdminClinic
        fields = '__all__'


