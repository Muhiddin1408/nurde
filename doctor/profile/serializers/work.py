from rest_framework import serializers

from apps.basic.models import Specialist
from apps.basic.models.work import WorkImage, Work


class FileWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkImage
        fields = ['id', 'file']
        read_only_fields = ['id']


class WorkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Work
        fields = ['id', 'type', 'name', 'education', 'finish' 'start']


    def create(self, validated_data):
        specialist = self.context['request'].user
        validated_data['specialist'] = Specialist.objects.get(user=specialist)
        education = super().create(validated_data)
        # for file_item in file_data:
        #     file = WorkImage.objects.get(id=file_item)
        #     file.education = education
        #     file.save()
        return education