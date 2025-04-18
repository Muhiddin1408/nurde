from django.db import transaction
from rest_framework import serializers
from django.core.exceptions import ValidationError

from apps.users.models import User


class NestedCreateMobileUserSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20, required=False)
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    middle_name = serializers.CharField(required=False, allow_blank=True)
    gen = serializers.CharField()
    lang = serializers.CharField(min_length=2, max_length=10, required=False)
    pin = serializers.IntegerField()
    email = serializers.EmailField()
    city = serializers.CharField()

    def validate_phone(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Phone already exist")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu email bilan foydalanuvchi allaqachon mavjud.")
        return value

    def validate_pin(self, value):
        if len(str(value)) != 14:
            raise serializers.ValidationError("PIN 14 ta raqamdan iborat bo'lishi kerak.")
        return value

    def validate(self, attrs):
        required_fields = ['phone', 'first_name', 'last_name', 'gen', 'pin', 'email', 'city']
        missing = [field for field in required_fields if not attrs.get(field)]
        if missing:
            raise serializers.ValidationError(f"Quyidagi maydonlar to‘ldirilishi shart: {', '.join(missing)}")
        return attrs


class RegisterSerializer(NestedCreateMobileUserSerializer):

    @transaction.atomic
    def save(self):
        validated_data = self.validated_data

        user = User.objects.create_user(
            username=validated_data.get('username'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            middle_name=validated_data.get('middle_name', ''),
            password=validated_data.get('password'),
            pin=validated_data.get('pin'),
            # city=validated_data.get('city'),
            # lang=validated_data.get('lang', 'uz'),
            # gen=validated_data.get('gen'),
        )
        return user


class PasswordSerializers(serializers.Serializer):
    password = serializers.CharField(min_length=3)
    confirm_password = serializers.CharField(min_length=3)
    phone = serializers.CharField(max_length=30, required=False)

    def validate(self, attrs):

            user = User.objects.get(username=attrs.get('phone'))
            if user and attrs.get('password') == attrs.get('confirm_password'):
                user.password = attrs.get('password')
                user.save()
            return attrs

