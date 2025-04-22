from rest_framework import serializers

from apps.basic.models import Specialist, CommentReadMore
from apps.basic.models.education import Education

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class SpecialistInfoSerializer(serializers.Serializer):
    info = serializers.CharField()
    education = serializers.SerializerMethodField()
    advanced = serializers.SerializerMethodField()

    class Meta:
        model = Specialist
        fields = ('info', 'education', 'advanced')
        read_only_fields = ('info', 'education', 'advanced')

    def get_education(self, obj):
        education = Education.objects.filter(specialist=obj, type='education')
        return EducationSerializer(education, many=True).data

    def get_advanced(self, obj):
        advanced = Education.objects.filter(specialist=obj, type='advanced')
        return EducationSerializer(advanced, many=True).data


class CommentReadMoreSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    comment = serializers.CharField()
    ranking = serializers.IntegerField()
    experts_response = serializers.CharField()
    costumer = serializers.SerializerMethodField()
    costumer_image = serializers.SerializerMethodField()

    class Meta:
        model = CommentReadMore
        fields = '__all__'

    def get_costumer(self, obj):
        return obj.user.user.last_name + " " + obj.user.user.first_name

    def get_costumer_image(self, obj):
        if obj.user.image:
            return obj.user.image.url
        return None

