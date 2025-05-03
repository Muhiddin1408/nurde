from django.db.models import Sum
from rest_framework import serializers

from apps.basic.models import CommentReadMore, Specialist


class RankingSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    ranking = serializers.SerializerMethodField()
    ranking_5 = serializers.SerializerMethodField()
    ranking_4 = serializers.SerializerMethodField()
    ranking_3 = serializers.SerializerMethodField()
    ranking_2 = serializers.SerializerMethodField()
    ranking_1 = serializers.SerializerMethodField()

    class Meta:
        model = Specialist
        fields = ('count', 'ranking', 'ranking_5', 'ranking_4', 'ranking_3', 'ranking_2', 'ranking_1')

    def get_ranking(self, obj):
        total = CommentReadMore.objects.filter(read_more=obj).aggregate(total=Sum('ranking'))['total'] or 0
        count = CommentReadMore.objects.filter(read_more=obj).count() or 1
        return round(total / count, 2)

    def get_ranking_5(self, obj):
        comment = CommentReadMore.objects.filter(read_more=obj, ranking=5).count()
        return comment

    def get_ranking_4(self, obj):
        comment = CommentReadMore.objects.filter(read_more=obj, ranking=4).count()
        return comment

    def get_ranking_3(self, obj):
        comment = CommentReadMore.objects.filter(read_more=obj, ranking=3).count()
        return comment

    def get_ranking_2(self, obj):
        comment = CommentReadMore.objects.filter(read_more=obj, ranking=2).count()
        return comment

    def get_ranking_1(self, obj):
        comment = CommentReadMore.objects.filter(read_more=obj, ranking=1).count()
        return comment

    def get_count(self, obj):
        return CommentReadMore.objects.filter(read_more=obj).count()
