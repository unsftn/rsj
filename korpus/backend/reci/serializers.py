import logging
from django.forms.models import model_to_dict
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

log = logging.getLogger(__name__)


class VarijantaImeniceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VarijantaImenice
        fields = ('id', 'redni_broj',
                  'nomjed', 'genjed', 'datjed', 'akujed', 'vokjed', 'insjed', 'lokjed', 
                  'nommno', 'genmno', 'datmno', 'akumno', 'vokmno', 'insmno', 'lokmno')


class IzmenaImeniceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IzmenaImenice
        fields = ('id', 'operacija_izmene', 'user', 'vreme')


class ImenicaSerializer(serializers.ModelSerializer):
    varijantaimenice_set = VarijantaImeniceSerializer(many=True, read_only=True)
    izmenaimenice_set = IzmenaImeniceSerializer(many=True, read_only=True)

    class Meta:
        model = Imenica
        fields = ('id', 'vrsta', 'recnik_id', 'status', 'vreme_kreiranja', 'poslednja_izmena', 
                  'nomjed', 'genjed', 'datjed', 'akujed', 'vokjed', 'insjed', 'lokjed', 
                  'nommno', 'genmno', 'datmno', 'akumno', 'vokmno', 'insmno', 'lokmno',
                  'varijantaimenice_set', 'izmenaimenice_set')


class NoSaveSerializer(serializers.Serializer):
    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        return instance


class SaveVarijantaImeniceSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    nomjed = serializers.CharField(max_length=50, allow_blank=True)
    genjed = serializers.CharField(max_length=50, allow_blank=True)
    datjed = serializers.CharField(max_length=50, allow_blank=True)
    akujed = serializers.CharField(max_length=50, allow_blank=True)
    vokjed = serializers.CharField(max_length=50, allow_blank=True)
    insjed = serializers.CharField(max_length=50, allow_blank=True)
    lokjed = serializers.CharField(max_length=50, allow_blank=True)
    nommno = serializers.CharField(max_length=50, allow_blank=True)
    genmno = serializers.CharField(max_length=50, allow_blank=True)
    datmno = serializers.CharField(max_length=50, allow_blank=True)
    akumno = serializers.CharField(max_length=50, allow_blank=True)
    vokmno = serializers.CharField(max_length=50, allow_blank=True)
    insmno = serializers.CharField(max_length=50, allow_blank=True)
    lokmno = serializers.CharField(max_length=50, allow_blank=True)


class SaveImenicaSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    vrsta = serializers.IntegerField(allow_null=True)
    nomjed = serializers.CharField(max_length=50, allow_blank=True)
    genjed = serializers.CharField(max_length=50, allow_blank=True)
    datjed = serializers.CharField(max_length=50, allow_blank=True)
    akujed = serializers.CharField(max_length=50, allow_blank=True)
    vokjed = serializers.CharField(max_length=50, allow_blank=True)
    insjed = serializers.CharField(max_length=50, allow_blank=True)
    lokjed = serializers.CharField(max_length=50, allow_blank=True)
    nommno = serializers.CharField(max_length=50, allow_blank=True)
    genmno = serializers.CharField(max_length=50, allow_blank=True)
    datmno = serializers.CharField(max_length=50, allow_blank=True)
    akumno = serializers.CharField(max_length=50, allow_blank=True)
    vokmno = serializers.CharField(max_length=50, allow_blank=True)
    insmno = serializers.CharField(max_length=50, allow_blank=True)
    lokmno = serializers.CharField(max_length=50, allow_blank=True)
    varijante = serializers.ListField(child=VarijantaImeniceSerializer())

    def create(self, validated_data):
        return self._save(validated_data)

    def update(self, instance, validated_data):
        VarijantaImenice.objects.filter(imenica_id=instance.id).delete()
        return self._save(validated_data, instance)

    def _save(self, validated_data, imenica=None):
        radimo_update = imenica is not None
        imenica_id = validated_data.get('id')
        sada = now()
        varijante = validated_data.pop('varijante', [])
        user = validated_data.pop('user')
        validated_data['poslednja_izmena'] = sada
        imenica, created = Imenica.objects.update_or_create(defaults=validated_data, id=imenica_id)
        for var in varijante:
            VarijantaImenice.objects.create(imenica=imenica, **var)
        operacija_izmene = 2 if radimo_update else 1
        IzmenaImenice.objects.create(user_id=user.id, vreme=sada, imenica=imenica, operacija_izmene=operacija_izmene)
        return imenica
