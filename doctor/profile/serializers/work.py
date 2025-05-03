from rest_framework import serializers

from apps.basic.models.work import WorkImage, Work


class FileWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkImage
        fields = ['id', 'file']
        read_only_fields = ['id']


class WorkSerializer(serializers.ModelSerializer):
    file = serializers.ListField(write_only=True)

    class Meta:
        model = Work
        fields = ['id', 'type', 'name', 'education', 'finish', 'specialist', 'file']

    def create(self, validated_data):
        file_data = validated_data.pop('file', [])
        education = super().create(validated_data)
        for file_item in file_data:
            WorkImage.objects.create(education=education, **file_item)
        return education