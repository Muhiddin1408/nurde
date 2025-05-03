from rest_framework import serializers

from apps.basic.models import Specialist
from apps.basic.models.education import Education, FileEducation


class FileEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileEducation
        fields = ['id', 'file']
        read_only_fields = ['id']


class EducationSerializer(serializers.ModelSerializer):
    file = serializers.ListField(write_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Education
        fields = ['id', 'type', 'name', 'education', 'finish', 'file', 'image']

    def get_image(self, obj):
        return FileEducationSerializer(FileEducation.objects.filter(education=obj), many=True, context=self.context).data

    def create(self, validated_data):
        file_data = validated_data.pop('file', [])
        specialist = self.context['request'].user
        validated_data['specialist'] = Specialist.objects.get(user=specialist)
        education = super().create(validated_data)
        for file_item in file_data:
            file = FileEducation.objects.get(id=file_item)
            file.education = education
            file.save()
        return education