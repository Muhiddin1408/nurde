from rest_framework import serializers

from apps.basic.models import Specialist
from apps.utils.models import Category
from doctor.auth.serializers.auth import CategorySerializer


class CategorySerializers(serializers.ModelSerializer):
    type = serializers.CharField()
    category = serializers.SerializerMethodField()
    experience = serializers.IntegerField()

    class Meta:
        model = Specialist
        fields = ('type', 'category', 'experience')

    def get_category(self, obj):
        return CategorySerializer(obj.category, many=True).data