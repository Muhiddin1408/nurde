from rest_framework import serializers

from apps.basic.models import Specialist


class ProfileSerializer(serializers.Serializer):
    photo = serializers.ImageField()
    last_name = serializers.CharField(source='user.last_name')
    first_name = serializers.CharField(source='user.first_name')
    middle_name = serializers.CharField(source='user.middle_name')
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    pinfl = serializers.CharField()

    class Meta:
        model = Specialist
        fields = '__all__'
