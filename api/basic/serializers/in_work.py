from rest_framework import serializers

from apps.basic.models.in_work import InWork


class InWorkSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    start = serializers.TimeField(read_only=True)
    finish = serializers.TimeField(read_only=True)
    weekday = serializers.CharField(read_only=True)

    class Meta:
        model = InWork
        fields = ('id', 'start', 'finish', 'weekday')
