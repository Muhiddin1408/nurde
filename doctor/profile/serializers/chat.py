from rest_framework import serializers

from apps.users.model.chat import MessageDoctor


class MessageDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageDoctor
        fields = ('id', 'content', 'file', 'status', 'created_at')
        read_only_fields = ('id',)

    def validate(self, attrs):
        content = attrs.get('content')
        file = attrs.get('file')

        if not content and not file:
            raise serializers.ValidationError("Content yoki File dan biri bo'lishi shart.")

        return attrs