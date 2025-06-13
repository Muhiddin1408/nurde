from rest_framework import serializers

from apps.basic.models import AdminClinic


class AdminClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminClinic
        fields = ['id', 'specialist', 'clinic', 'type', 'status', 'phone', 'email']