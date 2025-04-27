from datetime import date

from django.db import transaction
from rest_framework import serializers

from api.auth.serializers.address import AddressSerializer
from api.basic.serializers.service import ServiceSerializer
from api.basic.serializers.specialist import SpecialistSerializers
from api.users.serializers.ankita import AnkitaSerializer
from apps.basic.models import Specialist
from apps.order.models import Order, OrderFile, Phone, Diagnosis, Recommendations
from apps.service.models.service import Service
from apps.users.model import Patient, Image, Address, Ankita


class MyOrderListSerializers(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    ankita = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'doctor', 'address', 'ankita', 'price', 'payment_status', 'category', 'type')

    def get_category(self, obj):
        return obj.doctor.category.name

    def get_type(self, obj):
        return obj.doctor.type

    def get_doctor(self, obj):
        full_name = f"{obj.doctor.user.last_name} {obj.doctor.user.first_name}"
        if obj.doctor.user.middle_name:
            full_name += f" {obj.doctor.user.middle_name}"
        return full_name

    def get_address(self, obj):
        return AddressSerializer(obj.address, context={'request': self.context['request']}).data

    def get_ankita(self, obj):
        full_name = f"{obj.ankita.last_name} {obj.ankita.first_name}"
        if obj.ankita.middle_name:
            full_name += f" {obj.ankita.middle_name}"
        return full_name


class MyOrderSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    specialist = serializers.SerializerMethodField()
    payment_status = serializers.BooleanField(read_only=True)
    address = serializers.SerializerMethodField()
    datetime = serializers.DateTimeField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    category = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    ankita = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    diagnosis = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'specialist', 'payment_status', 'address', 'datetime', 'created_at', 'price',
                  'category', 'type', 'ankita', 'service', 'payment_type', 'image', 'diagnosis')

    def get_specialist(self, obj):
        request = self.context.get('request')
        full_name = f"{obj.doctor.user.last_name} {obj.doctor.user.first_name}"
        if obj.doctor.user.middle_name:
            full_name += f" {obj.doctor.user.middle_name}"
        photo_url = None
        if obj.doctor.photo:
            photo_url = request.build_absolute_uri(obj.doctor.photo.url)

        return {"full_name": full_name, "photo": photo_url}


    def get_address(self, obj):
        return AddressSerializer(obj.address, context={'request': self.context['request']}).data

    def get_category(self, obj):
        return obj.doctor.category.name

    def get_type(self, obj):
        return obj.doctor.type

    def get_ankita(self, obj):
        return AnkitaSerializer(obj.ankita, context={'request': self.context['request']}).data

    def get_service(self, obj):
        return ServiceSerializer(obj.service.all(), many=True, context={'request': self.context['request']}).data

    def get_image(self, obj):
        return OrderFileSerializer(obj.image.all(), many=True, context={'request': self.context['request']}).data

    def get_diagnosis(self, obj):
        diagnosis = Diagnosis.objects.filter(order=obj)
        if diagnosis.exists():
            return DiagnosisSerializers(diagnosis, many=True, context={'request': self.context['request']}).data
        return None





from rest_framework import serializers


class OrderSerializers(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Service.objects.all()
    )
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=Specialist.objects.all()
    )
    address = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all()
    )
    ankita = serializers.PrimaryKeyRelatedField(
        queryset=Ankita.objects.all(),
        allow_null=True,
        required=False
    )
    phone_numbers = serializers.ListField(
        child=serializers.CharField(max_length=20),
        write_only=True,
        required=False
    )
    image = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=OrderFile.objects.all()
    )

    class Meta:
        model = Order
        fields = [
            'id',
            'doctor',
            'address',
            'payment_status',
            'payment_type',
            'status',
            'datetime',
            'created_at',
            'image',
            'ankita',
            'service',
            'phone',
            'phone_numbers',
            'price'
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        uploaded_files = validated_data.pop('image', [])
        service_data = validated_data.pop('service', [])
        phone_numbers = validated_data.pop('phone_numbers', [])
        price = 0
        for i in service_data:
            service = Service.objects.get(id=i)
            price += service.price

        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            patient = Patient.objects.filter(user=request.user).last()
            validated_data['customer'] = patient

        order = Order.objects.create(**validated_data)

        if service_data:
            order.service.set(service_data)

        phone_instances = []
        for number in phone_numbers:
            phone_instance = Phone.objects.create(phone=number)
            phone_instances.append(phone_instance)

        order.phone.set(phone_instances)

        # Fayllarni saqlash
        if uploaded_files:
            order.image.set(uploaded_files)
        order.price = price
        order.save()
        return order


class OrderFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderFile
        fields = '__all__'


class DiagnosisSerializers(serializers.ModelSerializer):
    costumer = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    recommendation = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Diagnosis
        fields = ('id', 'costumer', 'age', 'recommendation', 'doctor', 'type', 'category', 'diagnosis', 'comment')

    def get_costumer(self, obj):
        return AnkitaSerializer(obj.order.ankita, context={'request': self.context['request']}).data

    def get_age(self, obj):
        today = date.today()
        age = today.year - obj.order.ankita.birthday.year - (
                (today.month, today.day) < (obj.order.ankita.birthday.month, obj.order.ankita.birthday.day)
        )
        return age

    def get_recommendation(self, obj):
        recommendation = Recommendations.objects.filter(diagnosis=obj)
        return RecommendationsSerializer(recommendation, many=True, context={'request': self.context['request']}).data

    def get_doctor(self, obj):
        full_name = f"{obj.order.doctor.user.last_name} {obj.order.doctor.user.first_name}"
        if obj.order.doctor.user.middle_name:
            full_name += f" {obj.order.doctor.user.middle_name}"
        return full_name

    def get_type(self, obj):
        return obj.order.doctor.type

    def get_category(self, obj):
        return obj.order.doctor.category.name


class RecommendationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendations
        fields = ('id', 'recommendation')
