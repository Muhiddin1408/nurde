from rest_framework import serializers

from apps.basic.models import Specialist
from apps.basic.models.work import WorkImage, Work


class FileWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkImage
        fields = ['id', 'file']
        read_only_fields = ['id']


class WorkSerializer(serializers.ModelSerializer):
    file = serializers.ListField(write_only=True)
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Work
        fields = ['id', 'type', 'name', 'education', 'finish',  'file', 'image', 'category']

    def get_image(self, obj):
        return FileWorkSerializer(WorkImage.objects.filter(education=obj), many=True, context=self.context).data

    def create(self, validated_data):
        file_data = validated_data.pop('file', [])
        specialist = self.context['request'].user
        validated_data['specialist'] = Specialist.objects.get(user=specialist)
        education = super().create(validated_data)
        for file_item in file_data:
            file = WorkImage.objects.get(id=file_item)
            file.education = education
            file.save()
        return education