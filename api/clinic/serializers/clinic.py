from rest_framework import serializers

from api.basic.serializers.comment import CommentSerializer
from apps.clinic.models import Clinic, Service
from apps.clinic.models.comment import Comment


class ClinicSerializers(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    address = serializers.CharField(read_only=True)
    image = serializers.SerializerMethodField()
    phone = serializers.CharField(read_only=True)
    class Meta:
        model = Clinic
        fields = ('id', 'name', 'address', 'phone', 'image')

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None


class ClinicDetailSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    address = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    image = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()

    class Meta:
        model = Clinic
        fields = '__all__'

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_comment(self, obj):
        comment = Comment.objects.filter(clinic_id=obj.id)
        return CommentSerializer(comment, many=True).data, comment.count()


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
