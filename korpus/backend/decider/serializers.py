from rest_framework import serializers
from .models import *


class GenerisaniSpisakSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenerisaniSpisak
        fields = ('id', 'start_time', 'end_time')


class RecZaOdlukuSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecZaOdluku
        fields = (
            'id', 'prvo_slovo', 'tekst', 'vrsta_reci', 'korpus_id', 
            'recnik_id', 'odluka', 'broj_publikacija', 'broj_pojavljivanja', 
            'vreme_odluke', 'donosilac_odluke', 'poslednje_generisanje')

    def update(self, instance, validated_data):
        # TODO: sacuvaj donosioca odluke i vreme odluke
        instance.odluka = validated_data['odluka']
        instance.save()
        return instance