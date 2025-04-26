from rest_framework import serializers

from api.basic.serializers.specialist import SpecialistSerializers
from apps.order.models import Order


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


class OrderSerializers(serializers.Serializer):

    class Meta:
        model = Order
        fields = '__all__'

