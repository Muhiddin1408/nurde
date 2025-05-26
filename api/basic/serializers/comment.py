from rest_framework import serializers

from api.basic.serializers.service import ServiceSerializer
from api.basic.serializers.specialist import SpecialistByIdSerializers, CategorySerializer
from apps.basic.models import CommentReadMore, CommentReadMoreLike, CommentReadMoreComment
from apps.clinic.models import Comment
from apps.order.models import Order


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = CommentReadMore
        fields = ('id', 'ranking', 'comment', 'user')

    def get_user(self, obj):
        return obj.user.lastname + " " + obj.user.firstname


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment', 'date', 'author', 'clinic', 'ranking', 'created_at']
        read_only_fields = ['created_at']


class MyCommentSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = CommentReadMore
        fields = ('id', 'ranking', 'comment', 'doctor', 'service', 'image', 'created_at')


    def get_doctor(self, obj):
        return obj.read_more.user.last_name + " " + obj.read_more.user.first_name

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.read_more:
            if obj.read_more.photo:
                return request.build_absolute_uri(obj.read_more.photo.url)
        return None


    def get_service(self, obj):
        if obj.order:
            return ServiceSerializer(obj.order.service.all(), many=True, context={'request': self.context['request']}).data
        return None



class WaitCommentSerializers(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'doctor')

    def get_doctor(self, obj):
        if obj.doctor:
            return SpecialistByIdSerializers(obj.doctor, context={'request': self.context['request']}).data
        return None




