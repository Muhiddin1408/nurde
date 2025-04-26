from django.db import transaction
from rest_framework import serializers

from api.basic.serializers.specialist import SpecialistSerializers
from apps.basic.models import Specialist
from apps.order.models import Order, OrderFile, Phone
from apps.service.models.service import Service
from apps.users.model import Patient, Image, Address, Ankita


class MyOrderSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    specialist = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    datetime = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'specialist', 'service', 'payment', 'address', 'datetime', 'created_at', 'costumer', 'file')

    def get_specialist(self, obj):
        return SpecialistSerializers(obj.specialist).data


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
    uploaded_files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
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
            'uploaded_files',
            'image',
            'ankita',
            'service',
            'phone',
            'phone_numbers'  # Bu joyni qo'shdik
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        uploaded_files = validated_data.pop('uploaded_files', [])
        service_data = validated_data.pop('service', [])
        phone_numbers = validated_data.pop('phone_numbers', [])

        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            patient = Patient.objects.filter(user=request.user).last()
            validated_data['customer'] = patient

        order = Order.objects.create(**validated_data)

        # service larni bog'lash
        if service_data:
            order.service.set(service_data)

        # Telefon raqamlarini yaratish va bog'lash
        phone_instances = []
        for number in phone_numbers:
            phone_instance = Phone.objects.create(phone=number)
            phone_instances.append(phone_instance)

        order.phone.set(phone_instances)

        # Fayllarni saqlash
        for file in uploaded_files:
            file_instance = OrderFile.objects.create(file=file)
            order.image.add(file_instance)

        return order