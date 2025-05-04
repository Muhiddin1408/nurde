from rest_framework import serializers

from apps.basic.models import Specialist
from apps.users.model.chat import MessageDoctor, ChatDoctor


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
    def create(self, validated_data):

        request = self.context['request']

        room = ChatDoctor.objects.filter(parent=Specialist.objects.filter(user=request.user).last()).last()
        if not room:
            room = ChatDoctor.objects.create(parent=Specialist.objects.filter(user=request.user).last(), name='')

        # yangi message yaratamiz
        message = MessageDoctor.objects.create(
            room=room,
            admin=None,
            content=validated_data.get('content'),
            file=validated_data.get('file'),
            status='user'
        )
        return message