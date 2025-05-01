from rest_framework import serializers

from apps.basic.models.education import Education, FileEducation


class FileEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileEducation
        fields = ['id', 'file']
        read_only_fields = ['id']


class EducationSerializer(serializers.ModelSerializer):
    file_education = FileEducationSerializer(many=True, read_only=True)

    class Meta:
        model = Education
        fields = ['id', 'type', 'name', 'education', 'finish', 'specialist', 'file_education']