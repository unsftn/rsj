from django.utils.timezone import now
from rest_framework import serializers
from .models import *


class VrstaPublikacijeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VrstaPublikacije
        fields = ('id', 'naziv')


class PotkorpusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Potkorpus
        fields = ('id', 'naziv')


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ('id', 'ime', 'prezime')


class TekstPublikacijeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TekstPublikacije
        fields = ('id', 'publikacija_id', 'redni_broj', 'tekst', 'tagovan_tekst')


class FajlPublikacijeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FajlPublikacije
        fields = ('id', 'publikacija_id', 'redni_broj', 'filename', 'url', 'extraction_status')


class ParametarFilteraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParametarFiltera
        fields = ('id', 'filter_id', 'redni_broj', 'naziv', 'vrednost')


class FilterPublikacijeSerializer(serializers.ModelSerializer):
    parametarfiltera_set = ParametarFilteraSerializer(many=True, read_only=True)

    class Meta:
        model = FilterPublikacije
        fields = ('id', 'publikacija_id', 'redni_broj', 'vrsta_filtera', 'parametarfiltera_set')


class PublikacijaSerializer(serializers.ModelSerializer):
    autor_set = AutorSerializer(many=True, read_only=True)
    fajlpublikacije_set = FajlPublikacijeSerializer(many=True, read_only=True)
    filterpublikacije_set = FilterPublikacijeSerializer(many=True, read_only=True)

    class Meta:
        model = Publikacija
        fields = ('id', 'naslov', 'naslov_izdanja', 'vrsta', 'isbn', 'issn',
                  'izdavac', 'godina', 'volumen', 'broj', 'url',
                  'vreme_unosa', 'autor_set', 'fajlpublikacije_set',
                  'user_id', 'skracenica', 'potkorpus', 'filterpublikacije_set',
                  'prevodilac', 'prvo_izdanje', 'napomena', 'zanr')


class NoSaveSerializer(serializers.Serializer):
    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        return instance


class CreateAutorSerializer(NoSaveSerializer):
    ime = serializers.CharField(max_length=50, required=False)
    prezime = serializers.CharField(max_length=50)


class SavePublikacijaSerializer(serializers.Serializer):
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
    vrsta_id = serializers.IntegerField(required=False, allow_null=True)
    potkorpus_id = serializers.IntegerField(required=False, allow_null=True)
    autori = serializers.ListField(child=CreateAutorSerializer())
    skracenica = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    prevodilac = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    prvo_izdanje = serializers.CharField(max_length=10, required=False, allow_blank=True, allow_null=True)
    napomena = serializers.CharField(max_length=1000, required=False, allow_blank=True, allow_null=True)
    zanr = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)

    def create(self, validated_data):
        return self._save(validated_data)

    def update(self, instance, validated_data):
        return self._save(validated_data, instance)

    def _save(self, validated_data, publikacija=None):
        radimo_update = publikacija is not None
        pub_id = validated_data.get('id')
        autori = validated_data.pop('autori', [])
        publikacija, created = Publikacija.objects.update_or_create(defaults=validated_data, id=pub_id)
        if radimo_update:
            Autor.objects.filter(publikacija=publikacija).delete()
        for index, autor in enumerate(autori):
            Autor.objects.create(publikacija=publikacija, redni_broj=index+1, **autor)
        return publikacija


class SaveTekstPublikacijeSerializer(serializers.Serializer):
    publikacija_id = serializers.IntegerField()
    redni_broj = serializers.IntegerField()
    tekst = serializers.CharField(allow_null=True, allow_blank=True)
    tagovan_tekst = serializers.CharField(allow_blank=True, allow_null=True)

    def create(self, validated_data):
        return self._save(validated_data)

    def update(self, instance, validated_data):
        return self._save(validated_data, instance)

    def _save(self, validated_data, tekst_publikacije=None):
        radimo_update = tekst_publikacije is not None
        tpid = validated_data.get('id')
        tekst_publikacije, created = TekstPublikacije.objects.update_or_create(defaults=validated_data, id=tpid)
        return tekst_publikacije
