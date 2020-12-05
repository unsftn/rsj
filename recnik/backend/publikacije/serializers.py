from rest_framework import serializers
from .models import *


class VrstaPublikacijeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VrstaPublikacije
        fields = ('id', 'naziv')


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ('id', 'ime', 'prezime')


class AutorPublikacijeSerializer(serializers.ModelSerializer):
    autor = AutorSerializer(read_only=True)

    class Meta:
        model = AutorPublikacije
        fields = ('id', 'autor', 'publikacija_id', 'redni_broj')


class TekstPublikacijeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TekstPublikacije
        fields = ('id', 'publikacija_id', 'redni_broj', 'tekst')


class FajlPublikacijeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FajlPublikacije
        fields = ('id', 'publikacija_id', 'redni_broj', 'uploaded_file')


class PublikacijaSerializer(serializers.ModelSerializer):
    vrsta = VrstaPublikacijeSerializer(read_only=True)
    autorpublikacije_set = AutorPublikacijeSerializer(many=True, read_only=True)

    class Meta:
        model = Publikacija
        fields = ('id', 'naslov', 'naslov_izdanja', 'vrsta', 'isbn', 'issn', 'izdavac', 'godina', 'volumen', 'broj',
                  'url', 'vreme_unosa', 'autorpublikacije_set')


