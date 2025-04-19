from rest_framework import serializers

from apps.clinic.models.comment import Comment


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='id')
    comment = serializers.CharField(source='comment')
    ranking = serializers.IntegerField(source='ranking')
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_user(self, obj):
        return obj.author.lastname + ' ' + obj.author.firstname
