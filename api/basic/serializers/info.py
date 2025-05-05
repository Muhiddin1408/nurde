from rest_framework import serializers

from apps.basic.models import Specialist, CommentReadMore
from apps.basic.models.education import Education
from apps.order.models import Order
from apps.users.model import Patient


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class SpecialistInfoSerializer(serializers.Serializer):
    info = serializers.CharField()
    education = serializers.SerializerMethodField()
    advanced = serializers.SerializerMethodField()

    class Meta:
        model = Specialist
        fields = ('info', 'education', 'advanced')
        read_only_fields = ('info', 'education', 'advanced')

    def get_education(self, obj):
        education = Education.objects.filter(specialist=obj, type='education')
        return EducationSerializer(education, many=True).data

    def get_advanced(self, obj):
        advanced = Education.objects.filter(specialist=obj, type='advanced')
        return EducationSerializer(advanced, many=True).data


class CommentReadMoreSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    comment = serializers.CharField()
    ranking = serializers.IntegerField()
    experts_response = serializers.CharField()
    costumer = serializers.SerializerMethodField()
    costumer_image = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()

    class Meta:
        model = CommentReadMore
        fields = '__all__'

    def get_costumer(self, obj):
        return obj.user.user.last_name + " " + obj.user.user.first_name

    def get_costumer_image(self, obj):
        request = self.context.get('request')
        if obj.user.image:
            return request.build_absolute_uri(obj.user.image.url)
            # return obj.user.image.url
        return None


class CommentReadMoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReadMore
        fields = [
            'id',
            'ranking',
            'comment',
            'service_rendered',
            'experts_response',
            'created_at',
            'order',
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        order_id = validated_data.pop('order')  # bu faqat ID
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise serializers.ValidationError({'order': 'Order not found'})

        # read_more ni Order orqali aniqlaymiz
        validated_data['read_more'] = order.doctor  # Order modelda `doctor` bor deb hisoblaymiz
        validated_data['order'] = order.id  # order obyektini qayta qo‘shamiz

        # user ni Patient orqali aniqlaymiz
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            patient = Patient.objects.filter(user=request.user).last()
            if not patient:
                raise serializers.ValidationError({'user': 'Patient not found'})
            validated_data['user'] = patient

        return super().create(validated_data)

