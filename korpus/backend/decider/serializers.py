from django.utils.timezone import now
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
            'vreme_odluke', 'donosilac_odluke', 'poslednje_generisanje',
            'beleska')

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            instance.donosilac_odluke = user
        instance.odluka = validated_data['odluka']
        instance.beleska = validated_data['beleska']
        instance.vreme_odluke = now()
        instance.save()
        return instance


class DinamickiIzvestajSerializer(serializers.ModelSerializer):
    class Meta:
        model = DinamickiIzvestaj
        fields = '__all__'
