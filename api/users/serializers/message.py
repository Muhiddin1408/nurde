
from rest_framework import serializers

from apps.users.model.chat import ChatRoom, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
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

        room = ChatRoom.objects.filter(parent=request.user).last()
        if not room:
            room = ChatRoom.objects.create(parent=request.user, name='')

        # yangi message yaratamiz
        message = Message.objects.create(
            room=room,
            admin=None,
            content=validated_data.get('content'),
            file=validated_data.get('file'),
            status=validated_data.get('user')
        )
        return message