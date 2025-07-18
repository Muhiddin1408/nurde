from datetime import datetime, timedelta

from django.db.models import Sum
from rest_framework import serializers

from api.basic.serializers.specialist import CategorySerializer
from apps.basic.models import AdminClinic, CommentReadMore
from doctor.clinic.views.worker import Worker


class WorkerSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    middle_name = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    # work_time = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    ranking = serializers.SerializerMethodField()
    # price = serializers.SerializerMethodField()
    # in_work = serializers.SerializerMethodField()
    # is_favorite = serializers.SerializerMethodField()
    experience = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    type_service = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Worker
        fields = (
            'id', 'last_name', 'first_name', 'middle_name',
            'experience', 'category', 'type', 'type_service', 'photo', 'comment',
            'ranking',
        )

    def get_experience(self, obj):
        return obj.specialist.experience

    def get_type_service(self, obj):
        return obj.specialist.type_service

    def get_photo(self, obj):
        request = self.context.get('request')  # Serializer contextdan requestni olamiz
        if obj.specialist.photo and request:
            return request.build_absolute_uri(obj.specialist.photo.url)
        return None
    def get_type(self, obj):
        return obj.specialist.type

    def get_id(self, obj):
        return obj.specialist.pk

    def get_last_name(self, obj):
        print(obj)
        return obj.specialist.user.last_name

    def get_first_name(self, obj):
        return obj.specialist.user.first_name

    def get_middle_name(self, obj):
        return obj.specialist.user.middle_name

    def get_category(self, obj):
        return CategorySerializer(obj.specialist.category, many=True).data

    # def get_work_time(self, obj):
    #     today = datetime.today().date()
    #     data = []
    #     for i in range(11):
    #         date = today + timedelta(days=i)
    #         time = []
    #         work_qs = WorkTime.objects.filter(user=obj.id, weekday__name=date.weekday())
    #         for i in work_qs:
    #             in_time = i.date
    #             if in_time is None:
    #                 in_time = dt_time(0, 0)
    #             now = datetime.now()
    #             combined_datetime = datetime.combine(date, in_time)
    #             book = Booked.objects.filter(worktime=i).exists()
    #             if not book and combined_datetime > now and not i.date is None:
    #                 time.append({'time': i.date})
    #
    #         data.append({'date': date, 'time': time})
    #
    #     return data

    def get_ranking(self, obj):
        total_ranking = CommentReadMore.objects.filter(read_more=obj.specialist).aggregate(Sum('ranking'))['ranking__sum'] or 0
        len = CommentReadMore.objects.filter(read_more=obj.specialist).count() or 1
        return total_ranking/len

    def get_comment(self, obj):
        comment = CommentReadMore.objects.filter(read_more=obj.specialist.id).count()
        return comment

    # def get_price(self, obj):
    #     service = Service.objects.filter(user=obj.id, status='active').order_by('price').first()
    #     if service:
    #         return ServiceSerializer(service).data
    #     return None

    # def get_in_work(self, obj):
    #     in_work = InWork.objects.filter(specialist=obj)
    #     return InWorkSerializer(in_work, many=True).data
