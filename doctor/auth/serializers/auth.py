import random

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from api.utils.eskiz import SendSmsApiWithEskiz
from apps.basic.models import Specialist
from apps.clinic.models import Clinic
from apps.users.models import User
from apps.utils.models import Category


class SpecialistSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    phone = serializers.CharField(max_length=110, source='user.username')
    last_name = serializers.CharField(max_length=125, source='user.last_name')
    first_name = serializers.CharField(max_length=125, source='user.first_name')
    middle_name = serializers.CharField(max_length=125, source='user.middle_name')
    lang = serializers.CharField(max_length=125, source='user.lang')
    birthday = serializers.DateField(source='user.birth_day')

    class Meta:
        model = Specialist
        fields = [
            'id',
            'pinfl',
            'gen',
            'city',
            'email',
            'phone',
            'last_name',
            'first_name',
            'middle_name',
            'lang',
            'birthday',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        user_data = validated_data.pop('user', {})

        # User uchun kerakli ma'lumotlar
        phone = user_data.get('username')
        email = user_data.get('email')
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')
        middle_name = user_data.get('middle_name', '')
        lang = user_data.get('lang', '')
        birthday = user_data.get('birthday')
        sms_code = random.randint(1000, 9999)
        if User.objects.filter(email=email).exists():
            raise ValidationError({'message': 'Email is already registered.'})
        if User.objects.filter(username=phone).exists():
            raise ValidationError({'message': 'Phone number is already registered.'})

        # Validating email and phone
        if not email:
            email = f"{phone}@example.com"  # Ensure phone is in correct format

        # Yangi user yaratish
        user = User.objects.filter(username=phone).last()
        if not user:
            user = User.objects.create(username=phone, email=email, last_name=last_name,
                                       first_name=first_name, middle_name=middle_name, lang=lang, birth_day=birthday)

        user.sms_code = sms_code
        user.save()
        SendSmsApiWithEskiz(message="https://star-one.uz/ Tasdiqlash kodi " + str(sms_code),
                            phone=int(phone)).send()

        specialist = Specialist.objects.create(user=user, **validated_data)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return specialist



from rest_framework import serializers

class SpecialistUpdateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='user.username', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    first_name = serializers.CharField(source='user.first_name', required=False)
    middle_name = serializers.CharField(source='user.middle_name', required=False)
    lang = serializers.CharField(source='user.lang', required=False)
    birthday = serializers.DateField(source='user.birthday', required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)

    class Meta:
        model = Specialist
        fields = [
            'id',
            'type',
            'photo',
            'category',
            'experience',
            'type_service',
            'staff',
            'info',
            'pinfl',
            'gen',
            'city',
            'password',

            'phone',
            'email',
            'last_name',
            'first_name',
            'middle_name',
            'lang',
            'birthday',
        ]
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        # Specialist modelini yangilash
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # User modelini yangilash
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        if 'category' in validated_data:
            instance.category.set(validated_data['category'])

        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

