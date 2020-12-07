from django.utils.timezone import now
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
    autor_set = AutorSerializer(many=True, read_only=True)

    class Meta:
        model = Publikacija
        fields = ('id', 'naslov', 'naslov_izdanja', 'vrsta', 'isbn', 'issn', 'izdavac', 'godina', 'volumen', 'broj',
                  'url', 'vreme_unosa', 'autor_set', 'user_id',)


class CreateAutorSerializer(serializers.Serializer):
    ime = serializers.CharField(max_length=50, required=False)
    prezime = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return Autor(**validated_data)

    def update(self, instance, validated_data):
        # nikad ne radimo update
        return instance


class CreatePublicationSerializer(serializers.Serializer):
    naslov = serializers.CharField(max_length=300)
    naslov_izdanja = serializers.CharField(max_length=300, required=False)
    isbn = serializers.CharField(max_length=13, required=False)
    issn = serializers.CharField(max_length=8, required=False)
    izdavac = serializers.CharField(max_length=200, required=False)
    godina = serializers.CharField(max_length=10, required=False)
    volumen = serializers.CharField(max_length=10, required=False)
    broj = serializers.CharField(max_length=10, required=False)
    url = serializers.URLField(max_length=500, required=False)
    vrsta_id = serializers.IntegerField()
    autori = CreateAutorSerializer(many=True, required=False)
    user_id = serializers.IntegerField()

    def create(self, validated_data):
        autori = validated_data['autori']
        del validated_data['autori']
        publikacija = Publikacija(**validated_data)
        publikacija.vreme_unosa = now()
        publikacija.save()
        for index, autor in enumerate(autori):
            pub_autor = Autor(**autor)
            pub_autor.publikacija = publikacija
            pub_autor.redni_broj = index + 1
            pub_autor.save()
        return publikacija

    def update(self, instance, validated_data):
        # nikad ne radimo update
        return instance


class CreateTextSerializer(serializers.Serializer):
    publikacija_id = serializers.IntegerField()
    tekst = serializers.CharField()
    redni_broj = serializers.IntegerField(required=False)

    def create(self, validated_data):
        tp = TekstPublikacije(**validated_data)
        if 'redni_broj' not in validated_data:
            max_broj = TekstPublikacije.objects.filter(publikacija_id=validated_data['publikacija_id']).count()
            tp.redni_broj = max_broj + 1
        tp.save()
        return tp

    def update(self, instance, validated_data):
        # nikad ne radimo update
        return instance
