from rest_framework import serializers

from apps.users.model.card import Card


class CardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

