from rest_framework import serializers

from apps.clinic.models import Clinic
from apps.service.models.service import WorkTime
from apps.users.model import Image
from doctor.profile.serializers.schedule import WorkTimeSerializer


class ClinicSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    address = serializers.CharField(read_only=True)
    image = serializers.SerializerMethodField()
    phone = serializers.CharField(read_only=True)
    category = serializers.CharField(read_only=True)
    latitude = serializers.FloatField(read_only=True)
    longitude = serializers.FloatField(read_only=True)
    description = serializers.CharField(read_only=True)

    types = serializers.SerializerMethodField()
    date = serializers.DateField(read_only=True)

    class Meta:
        model = Clinic
        fields = ('id', 'name', 'address', 'phone', 'image', 'category', 'latitude', 'longitude', 'description',
                  'types', 'date')

    def get_image(self, obj):
        request = self.context.get('request')  # request ni olib olamiz
        image = Image.objects.filter(clinic=obj).first()
        if image and image.image:
            if request is not None:
                return request.build_absolute_uri(image.image.url)  # to'liq URL yasaydi
            return image.image.url  # fallback
        return None

    def get_types(self, obj):
        if obj.types:
            return obj.types.name
        return None

    def get_date(self, obj):
        work = WorkTime.objects.filter(clinic=obj, user=None)
        if work:
            return WorkTimeSerializer(work, many=True).data
        return None
