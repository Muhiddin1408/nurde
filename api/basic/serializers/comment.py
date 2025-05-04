from rest_framework import serializers

from api.basic.serializers.service import ServiceSerializer
from api.basic.serializers.specialist import SpecialistByIdSerializers
from apps.basic.models import CommentReadMore
from apps.order.models import Order


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = CommentReadMore
        fields = ('id', 'ranking', 'comment', 'user')

    def get_user(self, obj):
        return obj.user.lastname + " " + obj.user.firstname


class MyCommentSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()

    class Meta:
        model = CommentReadMore
        fields = ('id', 'ranking', 'comment', 'doctor', 'service')

    def get_doctor(self, obj):
        return obj.read_more.user.last_name + " " + obj.read_more.user.first_name

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




