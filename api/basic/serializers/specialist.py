from django.db.models import Sum
from rest_framework import serializers
from datetime import datetime, timedelta
from datetime import time as dt_time
from api.basic.serializers.in_work import InWorkSerializer
from api.basic.serializers.info import EducationSerializer
from api.basic.serializers.service import ServiceSerializer
from apps.basic.models import Specialist, CommentReadMore, Worker
from apps.basic.models.education import Education
from apps.basic.models.in_work import InWork
from apps.basic.models.work import Work
from apps.service.models.booked import Booked
from apps.service.models.service import WorkTime, Service
from apps.utils.models import Category
from apps.utils.models.like import Like
from doctor.profile.serializers.work import WorkSerializer
from apps.clinic.models.service import Service as ClinicService


class WorkTimeSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()

    class Meta:
        model = WorkTime
        fields = ('time',)


class CategorySerializers(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    icon = serializers.FileField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'icon')
        # ref_name = "SpecialistCategorySerializer"

    def get_icon(self, obj):
        print(obj)
        return obj.icon.url


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class SpecialistSerializers(serializers.ModelSerializer):
    last_name = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    middle_name = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    work_time = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    ranking = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    in_work = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Specialist
        fields = (
            'id', 'last_name', 'first_name', 'middle_name', 'price',
            'experience', 'category', 'type', 'type_service', 'photo', 'work_time', 'comment',
            'ranking', 'in_work', 'is_favorite'
        )

    def get_last_name(self, obj):
        print(obj)
        return obj.user.last_name

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_middle_name(self, obj):
        return obj.user.middle_name

    def get_category(self, obj):
        return CategorySerializer(obj.category, many=True).data

    def get_work_time(self, obj):
        today = datetime.today().date()
        data = []
        for i in range(11):
            date = today + timedelta(days=i)
            time = []
            work_qs = WorkTime.objects.filter(user=obj.id, weekday__name=date.weekday())
            for i in work_qs:
                in_time = i.date
                if in_time is None:
                    in_time = dt_time(0, 0)
                now = datetime.now()
                combined_datetime = datetime.combine(date, in_time)
                book = Booked.objects.filter(worktime=i).exists()
                if not book and combined_datetime > now and not i.date is None:
                    time.append({'time': i.date})

            data.append({'date': date, 'time': time})

        return data

    def get_ranking(self, obj):
        total_ranking = CommentReadMore.objects.filter(read_more=obj).aggregate(Sum('ranking'))['ranking__sum'] or 0
        len = CommentReadMore.objects.filter(read_more=obj).count() or 1
        return total_ranking/len

    def get_comment(self, obj):
        comment = CommentReadMore.objects.filter(read_more=obj.id).count()
        return comment

    def get_price(self, obj):
        service = Service.objects.filter(user=obj.id, status='active').order_by('price').first()
        if service:
            return ServiceSerializer(service).data
        return None

    def get_in_work(self, obj):
        in_work = InWork.objects.filter(specialist=obj)
        return InWorkSerializer(in_work, many=True).data

    def get_is_favorite(self, obj):
        user = self.context['request']
        if not user.user.is_authenticated:
            return False
        is_favorite = Like.objects.filter(user=obj, costumer__user=user.user).exists()
        return is_favorite


class WorkerByIDSerializers(serializers.ModelSerializer):
    clinic = serializers.SerializerMethodField(read_only=True)
    service = serializers.SerializerMethodField(read_only=True)
    date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Worker
        fields = ('clinic', 'service',)

    def get_clinic(self, obj):
        return obj.clinic.name

    def get_service(self, obj):
        service = ClinicService.objects.filter(clinic=obj.clinic, status='active').first()
        return ServiceSerializer(service, many=True).data

    def get_date(self, obj):
        today = datetime.today().date()

        data = []
        for i in range(11):
            date = today + timedelta(days=i)
            time = []
            work_qs = WorkTime.objects.filter(user=obj.user, weekday__name=date.weekday(), clinic=obj.clinic)
            for i in work_qs:
                in_time = i.date
                if in_time is None:
                    in_time = dt_time(0, 0)
                now = datetime.now()
                combined_datetime = datetime.combine(date, in_time)
                book = Booked.objects.filter(worktime=i).exists()
                if not book and combined_datetime > now and not i.date is None:
                    time.append({'time': i.date})
            data.append({'date': date, 'time': time})
        return data



class SpecialistByIdSerializers(serializers.ModelSerializer):
    last_name = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    middle_name = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    work_time = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    ranking = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    in_work = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    info = serializers.CharField()
    education = serializers.SerializerMethodField()
    clinic = serializers.SerializerMethodField()

    class Meta:
        model = Specialist
        fields = (
            'id', 'last_name', 'first_name', 'middle_name', 'service', 'price',
            'experience', 'category', 'type', 'type_service', 'photo', 'work_time', 'comment',
            'ranking', 'in_work', 'is_favorite', 'education', 'info', 'description', 'clinic'
        )


    def get_last_name(self, obj):
        return obj.user.last_name

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_middle_name(self, obj):
        return obj.user.middle_name

    def get_category(self, obj):
        return CategorySerializer(obj.category, many=True).data

    def get_work_time(self, obj):
        today = datetime.today().date()

        data = []
        for i in range(11):
            date = today + timedelta(days=i)
            time = []
            work_qs = WorkTime.objects.filter(user=obj.id, weekday__name=date.weekday(), clinic=None)
            for i in work_qs:
                in_time = i.date
                if in_time is None:
                    in_time = dt_time(0,0)
                now = datetime.now()
                combined_datetime = datetime.combine(date, in_time)
                book = Booked.objects.filter(worktime=i).exists()
                if not book and combined_datetime > now and not i.date is None:
                    time.append({'time': i.date})

            data.append({'date': date, 'time': time})
        return data

    def get_ranking(self, obj):
        total_ranking = CommentReadMore.objects.filter(read_more=obj).aggregate(Sum('ranking'))['ranking__sum'] or 0
        len = CommentReadMore.objects.filter(read_more=obj).count() or 1
        return total_ranking/len

    def get_comment(self, obj):
        comment = CommentReadMore.objects.filter(read_more=obj.id).count()
        return comment

    def get_price(self, obj):
        service = Service.objects.filter(user=obj.id, status='active').order_by('price').first()
        if service:
            return ServiceSerializer(service).data
        return None

    def get_service(self, obj):
        service = Service.objects.filter(user=obj.id, status='active')
        return ServiceSerializer(service, many=True).data

    def get_in_work(self, obj):
        in_work = Work.objects.filter(specialist=obj)
        return WorkSerializer(in_work, many=True).data

    def get_is_favorite(self, obj):
        user = self.context['request']
        if not user.user.is_authenticated:
            return False
        is_favorite = Like.objects.filter(user=obj, costumer__user=user.user).exists()
        return is_favorite

    def get_education(self, obj):
        education = Education.objects.filter(specialist=obj)
        return EducationSerializer(education, many=True).data

    def get_clinic(self, obj):
        request = self.context['request']
        work = Worker.objects.filter(specialist=obj)
        if work:
            return WorkerByIDSerializers(work, many=True, context={"request": request})
        return None
