from rest_framework import serializers
from .models import Filial, TalimTuri, TalimShakli, Yonalish

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
