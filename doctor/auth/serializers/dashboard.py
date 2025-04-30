from rest_framework import serializers

from apps.clinic.models import Clinic
from apps.order.models import Order


class OrderDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class DashboardSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    address = serializers.CharField()
    challenges = serializers.SerializerMethodField()
    challenges_count = serializers.SerializerMethodField()

    class Meta:
        model = Clinic
        fields = '__all__'

    def get_challenges(self, obj):
        user = self.context['request'].user
        order = Order.objects.filter(doctor__user=user, clinic=obj)
        return OrderDoctorSerializer(order, many=True).data

    def get_challenges_count(self, obj):
        user = self.context['request'].user
        order = Order.objects.filter(doctor__user=user, clinic=obj)
        return order.count()
