import logging
from django.forms.models import model_to_dict
from rest_framework import serializers
from rest_framework.fields import ListField

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
                  'varijantaimenice_set', 'izmenaimenice_set', 'osnovni_oblik', 'vrsta_reci', 'naziv_vrste_reci')


class VarijantaGlagolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VarijanteGlagola
        fields = ('id', 'varijanta', 'tekst')


class IzmenaGlagolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IzmenaGlagola
        fields = ('id', 'operacija_izmene', 'user', 'vreme')


class OblikGlagolaSerializer(serializers.ModelSerializer):
    varijanteglagola_set = VarijantaGlagolaSerializer(many=True, read_only=True)

    class Meta:
        model = OblikGlagola
        fields = ('id', 'vreme', 'jd1', 'jd2', 'jd3', 'mn1', 'mn2', 'mn3', 'varijanteglagola_set')


class GlagolSerializer(serializers.ModelSerializer):
    oblikglagola_set = OblikGlagolaSerializer(many=True, read_only=True)

    class Meta:
        model = Glagol
        fields = ('id', 'gl_vid', 'gl_rod', 'infinitiv', 'recnik_id', 'status', 'vreme_kreiranja', 'poslednja_izmena',
                  'rgp_mj', 'rgp_zj', 'rgp_sj', 'rgp_mm', 'rgp_zm', 'rgp_sm', 'gpp', 'gps', 'oblikglagola_set',
                  'osnovni_oblik', 'vrsta_reci', 'naziv_vrste_reci')


class VidPridevaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VidPrideva
        fields = ('id', 'vid', 
                  'mnomjed', 'mgenjed', 'mdatjed', 'makujed', 'mvokjed', 'minsjed', 'mlokjed',
                  'mnommno', 'mgenmno', 'mdatmno', 'makumno', 'mvokmno', 'minsmno', 'mlokmno',
                  'znomjed', 'zgenjed', 'zdatjed', 'zakujed', 'zvokjed', 'zinsjed', 'zlokjed',
                  'znommno', 'zgenmno', 'zdatmno', 'zakumno', 'zvokmno', 'zinsmno', 'zlokmno',
                  'snomjed', 'sgenjed', 'sdatjed', 'sakujed', 'svokjed', 'sinsjed', 'slokjed',
                  'snommno', 'sgenmno', 'sdatmno', 'sakumno', 'svokmno', 'sinsmno', 'slokmno')


class PridevSerializer(serializers.ModelSerializer):
    vidprideva_set = VidPridevaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Pridev
        fields = ('id', 'recnik_id', 'status', 'vreme_kreiranja', 'poslednja_izmena', 'vidprideva_set',
                  'osnovni_oblik', 'vrsta_reci', 'naziv_vrste_reci')


class IzmenaPredlogaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IzmenaPredloga
        fields = ('id', 'operacija_izmene', 'user', 'vreme')


class PredlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predlog
        fields = ('id', 'tekst')


class IzmenaRecceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IzmenaRecce
        fields = ('id', 'operacija_izmene', 'user', 'vreme')


class ReccaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recca
        fields = ('id', 'tekst')
        

class IzmenaUzvikaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IzmenaUzvika
        fields = ('id', 'operacija_izmene', 'user', 'vreme')


class UzvikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uzvik
        fields = ('id', 'tekst')
        

class IzmenaVeznikaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IzmenaVeznika
        fields = ('id', 'operacija_izmene', 'user', 'vreme')


class VeznikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veznik
        fields = ('id', 'tekst')
        

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
    # TODO recnik_id, status

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


class SaveVarijantaGlagolaSerializer(NoSaveSerializer):
    varijanta = serializers.IntegerField(required=False)
    tekst = serializers.CharField(max_length=50, allow_blank=True)


class SaveOblikGlagolaSerializer(NoSaveSerializer):
    vreme = serializers.IntegerField(required=False)
    jd1 = serializers.CharField(max_length=50, allow_blank=True)
    jd2 = serializers.CharField(max_length=50, allow_blank=True)
    jd3 = serializers.CharField(max_length=50, allow_blank=True)
    mn1 = serializers.CharField(max_length=50, allow_blank=True)
    mn2 = serializers.CharField(max_length=50, allow_blank=True)
    mn3 = serializers.CharField(max_length=50, allow_blank=True)
    varijante = serializers.ListField(child=SaveVarijantaGlagolaSerializer())


class SaveGlagolSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    gl_rod = serializers.IntegerField(allow_null=True)
    gl_vid = serializers.IntegerField(allow_null=True)
    infinitiv = serializers.CharField(max_length=50, allow_blank=True)
    rgp_mj = serializers.CharField(max_length=50, allow_blank=True)
    rgp_zj = serializers.CharField(max_length=50, allow_blank=True)
    rgp_sj = serializers.CharField(max_length=50, allow_blank=True)
    rgp_mm = serializers.CharField(max_length=50, allow_blank=True)
    rgp_zm = serializers.CharField(max_length=50, allow_blank=True)
    rgp_sm = serializers.CharField(max_length=50, allow_blank=True)
    gpp = serializers.CharField(max_length=50, allow_blank=True)
    gps = serializers.CharField(max_length=50, allow_blank=True)
    oblici = serializers.ListField(child=SaveOblikGlagolaSerializer())

    def create(self, validated_data):
        return self._save(validated_data)

    def update(self, instance, validated_data):
        OblikGlagola.objects.filter(glagol_id=instance.id).delete()
        return self._save(validated_data, instance)

    def _save(self, validated_data, glagol=None):
        radimo_update = glagol is not None
        glagol_id = validated_data.get('id')
        sada = now()
        oblici = validated_data.pop('oblici', [])
        user = validated_data.pop('user')
        validated_data['poslednja_izmena'] = sada
        glagol, created = Glagol.objects.update_or_create(defaults=validated_data, id=glagol_id)
        for oblik in oblici:
            varijante = oblik.pop('varijante', [])
            oblik = OblikGlagola.objects.create(glagol=glagol, **oblik)
            for var in varijante:
                VarijanteGlagola.objects.create(oblik_glagola=oblik, **var)
        operacija_izmene = 2 if radimo_update else 1
        IzmenaGlagola.objects.create(user_id=user.id, vreme=sada, glagol=glagol, operacija_izmene=operacija_izmene)
        return glagol


class SaveVidPridevaSerializer(NoSaveSerializer):
    vid = serializers.IntegerField(required=False)
    mnomjed = serializers.CharField(max_length=25, allow_blank=True)
    mgenjed = serializers.CharField(max_length=25, allow_blank=True)
    mdatjed = serializers.CharField(max_length=25, allow_blank=True)
    makujed = serializers.CharField(max_length=25, allow_blank=True)
    mvokjed = serializers.CharField(max_length=25, allow_blank=True)
    minsjed = serializers.CharField(max_length=25, allow_blank=True)
    mlokjed = serializers.CharField(max_length=25, allow_blank=True)
    mnommno = serializers.CharField(max_length=25, allow_blank=True)
    mgenmno = serializers.CharField(max_length=25, allow_blank=True)
    mdatmno = serializers.CharField(max_length=25, allow_blank=True)
    makumno = serializers.CharField(max_length=25, allow_blank=True)
    mvokmno = serializers.CharField(max_length=25, allow_blank=True)
    minsmno = serializers.CharField(max_length=25, allow_blank=True)
    mlokmno = serializers.CharField(max_length=25, allow_blank=True)
    znomjed = serializers.CharField(max_length=25, allow_blank=True)
    zgenjed = serializers.CharField(max_length=25, allow_blank=True)
    zdatjed = serializers.CharField(max_length=25, allow_blank=True)
    zakujed = serializers.CharField(max_length=25, allow_blank=True)
    zvokjed = serializers.CharField(max_length=25, allow_blank=True)
    zinsjed = serializers.CharField(max_length=25, allow_blank=True)
    zlokjed = serializers.CharField(max_length=25, allow_blank=True)
    znommno = serializers.CharField(max_length=25, allow_blank=True)
    zgenmno = serializers.CharField(max_length=25, allow_blank=True)
    zdatmno = serializers.CharField(max_length=25, allow_blank=True)
    zakumno = serializers.CharField(max_length=25, allow_blank=True)
    zvokmno = serializers.CharField(max_length=25, allow_blank=True)
    zinsmno = serializers.CharField(max_length=25, allow_blank=True)
    zlokmno = serializers.CharField(max_length=25, allow_blank=True)
    snomjed = serializers.CharField(max_length=25, allow_blank=True)
    sgenjed = serializers.CharField(max_length=25, allow_blank=True)
    sdatjed = serializers.CharField(max_length=25, allow_blank=True)
    sakujed = serializers.CharField(max_length=25, allow_blank=True)
    svokjed = serializers.CharField(max_length=25, allow_blank=True)
    sinsjed = serializers.CharField(max_length=25, allow_blank=True)
    slokjed = serializers.CharField(max_length=25, allow_blank=True)
    snommno = serializers.CharField(max_length=25, allow_blank=True)
    sgenmno = serializers.CharField(max_length=25, allow_blank=True)
    sdatmno = serializers.CharField(max_length=25, allow_blank=True)
    sakumno = serializers.CharField(max_length=25, allow_blank=True)
    svokmno = serializers.CharField(max_length=25, allow_blank=True)
    sinsmno = serializers.CharField(max_length=25, allow_blank=True)
    slokmno = serializers.CharField(max_length=25, allow_blank=True)


class SavePridevSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    vidovi = serializers.ListField(child=SaveVidPridevaSerializer())

    def create(self, validated_data):
        return self._save(validated_data)

    def update(self, instance, validated_data):
        VidPrideva.objects.filter(pridev_id=instance.id).delete()
        return self._save(validated_data, instance)

    def _save(self, validated_data, pridev=None):
        radimo_update = pridev is not None
        pridev_id = validated_data.get('id')
        sada = now()
        vidovi = validated_data.pop('vidovi', [])
        user = validated_data.pop('user')
        validated_data['poslednja_izmena'] = sada
        pridev, created = Pridev.objects.update_or_create(defaults=validated_data, id=pridev_id)
        for v in vidovi:
            VidPrideva.objects.create(pridev=pridev, **v)
        operacija_izmene = 2 if radimo_update else 1
        IzmenaPrideva.objects.create(user_id=user.id, vreme=sada, pridev=pridev, operacija_izmene=operacija_izmene)
        return pridev
