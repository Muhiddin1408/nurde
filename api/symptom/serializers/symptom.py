from rest_framework import serializers

from apps.clinic.models import Symptom, SymptomType, SymptomSubType


class SymptomSubTypeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()

    class Meta:
        model = SymptomSubType
        fields = ('id', 'name')


class SymptomTypeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    symptom_sub = serializers.SerializerMethodField()

    class Meta:
        model = SymptomType
        fields = ('id', 'name', 'description', 'symptom_sub', 'category')
    
    def get_symptom_sub(self, obj):
        query = SymptomSubType.objects.filter(symptom_id=obj.id)

        return SymptomSubTypeSerializer(query, many=True).data


class SymptomSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    info = serializers.SerializerMethodField()

    class Meta:
        model = Symptom
        fields = ('id', 'name', 'description', 'info')
        read_only_fields = ('id',)

    def get_name(self, obj):
        request = self.context.get('request')
        if request:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'uz')
            language = language.split('-')[0].split(',')[0].lower()
            if language == 'ru' and obj.name_ru:
                return obj.name_ru
            elif language == 'en' and obj.name_en:
                return obj.name_en
            else:
                return obj.name

    def get_info(self, obj):
        request = self.context.get('request')
        type_param = request.query_params.get('type') if request else None

        if type_param in ['review', 'reasons', 'treatment', 'treats']:
            data = SymptomType.objects.filter(type=type_param, symptom_id=obj.id)
            return SymptomTypeSerializer(data, many=True).data
        return []


