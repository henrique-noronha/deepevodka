from rest_framework import serializers
from .models import Evento, SetMusical


class SerializadorEvento(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'


class SerializadorSet(serializers.ModelSerializer):
    class Meta:
        model = SetMusical
        fields = '__all__'
