from rest_framework import serializers

from apps.basic.models import CommentReadMore


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = CommentReadMore
        fields = ('id', 'ranking', 'comment', 'user')

    def get_user(self, obj):
        return obj.user.lastname + " " + obj.user.firstname

