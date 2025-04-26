from rest_framework import serializers

from apps.users.model.image import Image


class ImageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image = serializers.ImageField()

    class Meta:
        model = Image
        fields = '__all__'