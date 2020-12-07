from rest_framework import serializers
from .models import *


class VrstaImeniceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VrstaImenice
        fields = ('id', 'naziv',)


class VarijantaImeniceSeralizer(serializers.ModelSerializer):
    class Meta:
        model = VarijantaImenice
        fields = ('id', 'imenica_id', 'redni_broj', 'nomjed', 'genjed', 'datjed', 'akujed', 'vokjed', 'insjed',
                  'lokjed', 'nommno', 'genmno', 'datmno', 'akumno', 'vokmno', 'insmno', 'lokmno',)


class IzmenaImeniceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IzmenaImenice
        fields = ('id', 'imenica_id', 'user_id', 'vreme',)


class ImenicaSerializer(serializers.ModelSerializer):
    vrsta = VrstaImeniceSerializer(read_only=True)
    varijantaimenice_set = VarijantaImeniceSeralizer(many=True, read_only=True)
    izmenaimenice_set = IzmenaImeniceSerializer(many=True, read_only=True)

    class Meta:
        model = Imenica
        fields = ('id', 'nomjed', 'genjed', 'datjed', 'akujed', 'vokjed', 'insjed', 'lokjed', 'nommno', 'genmno',
                  'datmno', 'akumno', 'vokmno', 'insmno', 'lokmno', 'vrsta', 'varijantaimenice_set',
                  'izmenaimenice_set', 'vreme', 'version',)


class OblikGlagolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OblikGlagola
        fields = ('id', 'glagol_id', 'vreme', 'jd1', 'jd2', 'jd3', 'mn1', 'mn2', 'mn3',)


class IzmenaGlagolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IzmenaGlagola
        fields = ('id', 'glagol_id', 'user_id', 'vreme',)


class GlagolSerializer(serializers.ModelSerializer):
    oblikglagola_set = OblikGlagolaSerializer(many=True, read_only=True)
    izmenaglagola_set = IzmenaGlagolaSerializer(many=True, read_only=True)

    class Meta:
        model = Glagol
        fields = ('id', 'infinitiv', 'rod', 'vid', 'rgp_mj', 'rgp_zj', 'rgp_sj', 'rgp_mm', 'rgp_zm', 'rgp_sm', 'gpp',
                  'gps', 'oblikglagola_set', 'izmenaglagola_set', 'vreme', 'version',)


class OblikPridevaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OblikPrideva
        fields = ('id', 'pridev_id', 'tekst', 'vid', 'rod', 'broj', 'padez',)


class IzmenaPridevaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IzmenaPrideva
        fields = ('id', 'pridev_id', 'user_id', 'vreme',)


class PridevSerializer(serializers.ModelSerializer):
    oblikprideva_set = OblikPridevaSerializer(many=True, read_only=True)
    izmenaprideva_set = IzmenaPridevaSerializer(many=True, read_only=True)

    class Meta:
        model = Pridev
        fields = ('id', 'tekst', 'oblikprideva_set', 'izmenaprideva_set', 'vreme', 'version',)


class CreateImenicaSerializer(serializers.Serializer):
    # TODO
    pass


class CreateGlagolSerializer(serializers.Serializer):
    # TODO
    pass


class CreatePridevSerializer(serializers.Serializer):
    # TODO
    pass
