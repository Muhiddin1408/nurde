from django.db import transaction
from rest_framework import serializers
from django.core.exceptions import ValidationError

from apps.users.models import User


class NestedCreateMobileUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, required=False)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exist")
        return value


class RegisterSerializer(NestedCreateMobileUserSerializer):

    @transaction.atomic
    def save(self):
        validated_data = self.validated_data
        print(self.validated_data)
        user = User.objects.create_user(
            username=validated_data.get('username')
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

