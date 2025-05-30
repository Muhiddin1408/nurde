from rest_framework import serializers

from apps.users.model import Ankita, Relative, Patient


class AnkitaSerializer(serializers.ModelSerializer):
    relative = serializers.PrimaryKeyRelatedField(
        queryset=Relative.objects.all()
    )
    relative_info = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Ankita
        fields = [
            'id',
            'name',
            'relative',
            'relative_info',
            'birthday',
            'gen',
            'height',
            'weight',
            'phone',
            'relative_text',
            'waist'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            patient = Patient.objects.filter(user=request.user).last()
            validated_data['user'] = patient
        return super().create(validated_data)

    def get_relative_info(self, obj):
        if obj.relative:
            return {
                'id': obj.relative.id,
                'name': obj.relative.name
            }
        return None


class RelativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relative
        fields = '__all__'
