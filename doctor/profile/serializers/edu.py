from rest_framework import serializers

from apps.basic.models.education import Education, FileEducation


class FileEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileEducation
        fields = ['id', 'file']
        read_only_fields = ['id']


class EducationSerializer(serializers.ModelSerializer):
    file = serializers.ListField(write_only=True)

    class Meta:
        model = Education
        fields = ['id', 'type', 'name', 'education', 'finish', 'file']

    def create(self, validated_data):
        file_data = validated_data.pop('file', [])
        specialist = self.context['request'].user
        validated_data['specialist'] = specialist
        education = super().create(validated_data)
        for file_item in file_data:
            FileEducation.objects.create(education=education, **file_item)
        return education