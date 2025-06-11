from rest_framework import serializers

from apps.utils.models.story import Story


class StorySerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = ['id', 'name', 'description', 'image', 'created_at', 'status']

    def get_status(self, obj):
        user = self.context['request'].user
        has_viewed = obj.storyview_set.filter(user=user).exists()
        return True if has_viewed else False
