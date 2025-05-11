from rest_framework import serializers

from apps.users.model import Patient


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    middle_name = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ('id', 'name', 'first_name', 'last_name', 'middle_name', 'phone', 'email', 'pinfl', 'image')

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_middle_name(self, obj):
        return obj.user.middle_name

    def get_phone(self, obj):
        return obj.user.phone[1:]

    def get_email(self, obj):
        return obj.user.email

    def get_name(self, obj):
        return obj.user.name


class ProfileUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    first_name = serializers.CharField(source='user.first_name', required=False)
    middle_name = serializers.CharField(source='user.middle_name', required=False)
    username = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email', required=False)

    class Meta:
        model = Patient
        fields = ('first_name', 'last_name', 'middle_name', 'username', 'email', 'pinfl', 'image', 'name')

    def get_username(self, obj):
        if obj.user and obj.user.username:
            return obj.user.username[1:]
        return ''

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                if attr == 'username':
                    setattr(user, attr, 'u' + value)
                else:
                    setattr(user, attr, value)
            user.save()

        return instance