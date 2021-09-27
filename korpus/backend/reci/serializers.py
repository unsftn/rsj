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
