from rest_framework import serializers

from api.order.serializers.order import OrderSerializers
from apps.basic.models import Specialist
from apps.clinic.models import Clinic
from apps.order.models import Order


class OrderDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class DashboardSerializer(serializers.ModelSerializer):
    wait = serializers.SerializerMethodField()

    class Meta:
        model = Specialist
        fields = ('wait', )

    def get_wait(self, obj):
        order = Order.objects.filter(doctor=obj, status='wait')
        return OrderSerializers(order, many=True, context={'request': self.context['request']}).data

