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
                  'url', 'vreme_unosa', 'autor_set', 'user_id', 'skracenica')


class CreateAutorSerializer(serializers.Serializer):
    ime = serializers.CharField(max_length=50, required=False)
    prezime = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return Autor(**validated_data)

    def update(self, instance, validated_data):
        # nikad ne radimo update
        return instance


class CreatePublicationSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    naslov = serializers.CharField(max_length=300)
    naslov_izdanja = serializers.CharField(max_length=300, required=False, allow_blank=True, allow_null=True)
    isbn = serializers.CharField(max_length=13, required=False, allow_blank=True, allow_null=True)
    issn = serializers.CharField(max_length=8, required=False, allow_blank=True, allow_null=True)
    izdavac = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True)
    godina = serializers.CharField(max_length=10, required=False, allow_blank=True, allow_null=True)
    volumen = serializers.CharField(max_length=10, required=False, allow_blank=True, allow_null=True)
    broj = serializers.CharField(max_length=10, required=False, allow_blank=True, allow_null=True)
    url = serializers.URLField(max_length=500, required=False, allow_blank=True, allow_null=True)
    vrsta_id = serializers.IntegerField()
    autori = CreateAutorSerializer(many=True, required=False)
    skracenica = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return self._save(validated_data)

    def update(self, instance, validated_data):
        return self._save(validated_data, instance)

    def _save(self, validated_data, publikacija=None):
        autori = validated_data.pop('autori', [])
        # user = validated_data.get('user')
        pub_id = validated_data.get('id')
        publikacija, created = Publikacija.objects.update_or_create(defaults=validated_data, id=pub_id)
        if not created:
            Autor.objects.filter(publikacija=publikacija).delete()
        for index, autor in enumerate(autori):
            Autor.objects.create(publikacija=publikacija, redni_broj=index+1, **autor)
        return publikacija


class CreateTextSerializer(serializers.Serializer):
    publikacija_id = serializers.IntegerField()
    tekst = serializers.CharField()

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
