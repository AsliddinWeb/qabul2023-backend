from rest_framework import serializers
from .models import Filial, TalimTuri, TalimShakli, Yonalish, RegisterSlayder

class FilialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filial
        fields = '__all__'

class TalimTuriSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalimTuri
        fields = '__all__'

class TalimShakliSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalimShakli
        fields = '__all__'

class YonalishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yonalish
        fields = '__all__'

class RegisterSlayderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterSlayder
        fields = '__all__'
