from rest_framework import serializers

from apps.clinic.models import Symptom, SymptomType, SymptomSubType


class SymptomSubTypeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()

    class Meta:
        model = SymptomSubType
        fields = ('id', 'name', 'category')


class SymptomTypeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    symptom_sub = serializers.SerializerMethodField()

    class Meta:
        model = SymptomType
        fields = ('id', 'name', 'description', 'symptom_sub')
    
    def get_symptom_sub(self, obj):
        query = SymptomSubType.objects.filter(symptom_id=obj.id)

        return SymptomSubTypeSerializer(query, many=True).data


class SymptomSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    info = serializers.SerializerMethodField()

    class Meta:
        model = Symptom
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)

    def get_info(self, obj):
        request = self.context.get('request')
        type_param = request.query_params.get('type') if request else None

        if type_param in ['review', 'reasons', 'treatment', 'treats']:
            data = SymptomType.objects.filter(type=type_param, symptom_id=obj.id)
            return SymptomTypeSerializer(data, many=True).data
        return []


