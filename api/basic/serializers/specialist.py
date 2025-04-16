from rest_framework import serializers

from apps.basic.models import Specialist
from apps.utils.models import Category


class CategorySerializers(serializers.Serializer):

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('id',)


class SpecialistSerializers(serializers.Serializer):
    last_name = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    middle_name = serializers.CharField(read_only=True)
    category = CategorySerializers(read_only=True)
    ranking = serializers.IntegerField(read_only=True)
    comment = serializers.IntegerField()

    class Meta:
        model = Specialist
        fields = ('id', 'last_name', 'first_name', 'middle_name', 'experience', 'category', 'ranking', 'comment')
