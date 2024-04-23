from rest_framework import serializers

from .models import DiplomMalumotTuri, DiplomMuassasaTuri, Kurslar, Diplom, PerevodDiplom

class DiplomMalumotTuriSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiplomMalumotTuri
        fields = '__all__'

class DiplomMuassasaTuriSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiplomMuassasaTuri
        fields = '__all__'

class KurslarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kurslar
        fields = '__all__'

class DiplomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diplom
        fields = '__all__'

class PerevodDiplomSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevodDiplom
        fields = '__all__'
