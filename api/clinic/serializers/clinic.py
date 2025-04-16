from rest_framework import serializers

from apps.clinic.models import Clinic, Service
from apps.clinic.models.comment import Comment


class ClinicSerializers(serializers.Serializer):

    class Meta:
        model = Clinic
        fields = '__all__'


class ClinicServiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class SpecialistServiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class CommentServiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
