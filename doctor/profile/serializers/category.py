from rest_framework import serializers

from apps.basic.models import Specialist
from apps.basic.models.education import Education
from apps.basic.models.work import Work
from apps.utils.models import Category
from doctor.auth.serializers.auth import CategorySerializer


class CategorySerializers(serializers.ModelSerializer):
    type = serializers.CharField()
    category = serializers.SerializerMethodField()
    work_count = serializers.SerializerMethodField()
    edu_count = serializers.SerializerMethodField()
    experience = serializers.IntegerField()

    class Meta:
        model = Specialist
        fields = ('type', 'category', 'experience', 'work_count', 'edu_count')

    def get_category(self, obj):
        return CategorySerializer(obj.category, many=True).data

    def get_work_count(self, obj):
        return Work.objects.filter(specialist=obj).count()

    def get_edu_count(self, obj):
        return Education.objects.filter(specialist=obj).count()