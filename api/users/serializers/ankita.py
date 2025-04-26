from rest_framework import serializers

from apps.users.model import Ankita, Relative, Patient


class AnkitaSerializer(serializers.ModelSerializer):
    relative = serializers.SerializerMethodField()

    class Meta:
        model = Ankita
        fields = [
            'id',
            'name',
            'relative',
            'birthday',
            'gen',
            'height',
            'weight',
            'phone',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            patient = Patient.objects.filter(user=request.user).last()
            validated_data['user'] = patient
        return super().create(validated_data)

    def get_relative(self, obj):
        return obj.relative.name


class RelativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relative
        fields = '__all__'
