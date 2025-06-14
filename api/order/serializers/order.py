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
    service = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    ankita_name = serializers.SerializerMethodField()
    clinic = serializers.SerializerMethodField()
    clinic_address = serializers.SerializerMethodField()
    clinic_phone = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'doctor', 'address', 'ankita_name', 'price', 'payment_status', 'service', 'type', 'datetime',
                  'clinic', 'clinic_address', 'clinic_phone')

    def get_service(self, obj):
        return ServiceSerializer(obj.service.all(), many=True, context={'request': self.context['request']}).data

    def get_type(self, obj):
        return obj.doctor.type

    def get_doctor(self, obj):
        full_name = f"{obj.doctor.user.last_name} {obj.doctor.user.first_name}"
        if obj.doctor.user.middle_name:
            full_name += f" {obj.doctor.user.middle_name}"
        return full_name

    def get_address(self, obj):
        return AddressSerializer(obj.address, context={'request': self.context['request']}).data

    def get_ankita_name(self, obj):

        return obj.ankita.name

    def get_clinic(self, obj):
        if obj.clinic:
            return obj.clinic.name
        return None

    def get_clinic_address(self, obj):
        if obj.clinic:
            return obj.clinic.address
        return None

    def get_clinic_phone(self, obj):
        if obj.clinic:
            return obj.clinic.phone
        return


class MyOrderSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    specialist = serializers.SerializerMethodField()
    payment_status = serializers.BooleanField(read_only=True)
    address = serializers.SerializerMethodField()
    datetime = serializers.DateTimeField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    type = serializers.SerializerMethodField()
    ankita = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    diagnosis = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'specialist', 'payment_status', 'address', 'datetime', 'created_at', 'price',
                'type', 'ankita', 'service', 'payment_type', 'image', 'diagnosis', 'result')

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
            return DiagnosisSerializer(diagnosis, many=True, context={'request': self.context['request']}).data
        return None

    def get_result(self, obj):
        result = Recommendations.objects.filter(order=obj)
        if result.exists():
            return RecommendationsSerializer(result, many=True, context={'request': self.context['request']}).data
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
        queryset=Address.objects.all(), required=False
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
            'datetime',
            'created_at',
            'image',
            'ankita',
            'service',
            'phone',
            'phone_numbers',
            'price',
            'clinic'
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        uploaded_files = validated_data.pop('image', [])
        service_data = validated_data.pop('service', [])
        phone_numbers = validated_data.pop('phone_numbers', [])
        price = 0
        for i in service_data:

            price += i.price

        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            patient = Patient.objects.filter(user=request.user).last()
            validated_data['customer'] = patient

        order = Order.objects.create(**validated_data)

        if service_data:
            order.service.set(service_data)

        phone_instances = []
        for number in phone_numbers:
            phone_instance, created = Phone.objects.get_or_create(phone=number)
            phone_instances.append(phone_instance)

        order.phone.set(phone_instances)
        if uploaded_files:
            order.image.set(uploaded_files)
        order.price = price
        order.save()
        return order


class OrderFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderFile
        fields = '__all__'


class DiagnosisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Diagnosis
        fields = ('id', 'comment')
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
    diagnosis = serializers.SerializerMethodField()

    class Meta:
        model = Recommendations
        fields = ('id', 'recommendation', 'result', 'diagnosis')

    def get_diagnosis(self, obj):
        return [{"id": symptom.id, "name": symptom.name} for symptom in obj.diagnosis.all()]

