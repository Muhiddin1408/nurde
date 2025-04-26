from django.db.models import Sum
from rest_framework import serializers

from api.basic.serializers.comment import CommentSerializer
from api.utils.serializsers.image import ImageSerializer
from apps.clinic.models import Clinic, Service
from apps.clinic.models.comment import Comment
from apps.users.model.image import Image
from apps.utils.models.like import Like


class ClinicSerializers(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    address = serializers.CharField(read_only=True)
    image = serializers.SerializerMethodField()
    phone = serializers.CharField(read_only=True)
    category = serializers.CharField(read_only=True)
    latitude = serializers.FloatField(read_only=True)
    longitude = serializers.FloatField(read_only=True)
    description = serializers.CharField(read_only=True)
    like = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    ranking = serializers.SerializerMethodField()
    types = serializers.SerializerMethodField()

    class Meta:
        model = Clinic
        fields = ('id', 'name', 'address', 'phone', 'image', 'category', 'latitude', 'longitude', 'description', 'like',
                  'comment', 'ranking', 'types')

    def get_image(self, obj):
        image = Image.objects.filter(clinic=obj)
        return ImageSerializer(image, many=True).data

    def get_like(self, obj):
        user = self.context['request'].user
        like = Like.objects.filter(clinic=obj, costumer__user=user)
        if like:
            return True
        else:
            return False
        
    def get_comment(self, obj):
        comment = Comment.objects.filter(clinic=obj).count()
        return comment

    def get_ranking(self, obj):
        comments = Comment.objects.filter(clinic=obj)
        total_ranking = comments.aggregate(Sum('ranking'))['ranking__sum'] or 0
        count = comments.count() or 1
        return total_ranking / count

    def get_types(self, obj):
        if obj.types:
            return obj.types.name
        return None


class ClinicDetailSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    address = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    image = serializers.ImageField(read_only=True)
    comment = serializers.SerializerMethodField()

    class Meta:
        model = Clinic
        fields = '__all__'

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
