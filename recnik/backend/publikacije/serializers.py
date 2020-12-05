from rest_framework import serializers
from .models import *


class VrstaPublikacijeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VrstaPublikacije
        fields = ('id', 'naziv')


class PublikacijaSerializer(serializers.ModelSerializer):
    vrsta = VrstaPublikacijeSerializer(read_only=True)

    class Meta:
        model = Publikacija
        fields = ('id', 'naslov', 'naslov_izdanja', 'vrsta', 'isbn', 'issn', 'izdavac', 'godina', 'volumen', 'broj',
                  'url', 'vreme_unosa')
