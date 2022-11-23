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
        fields = ('id', 'vrsta', 'recnik_id', 'status', 'vreme_kreiranja', 'poslednja_izmena', 'vlasnik',
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
                  'osnovni_oblik', 'vrsta_reci', 'naziv_vrste_reci', 'vlasnik')


# class VidPridevaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VidPrideva
#         fields = ('id', 'vid', 
#                   'mnomjed', 'mgenjed', 'mdatjed', 'makujed', 'mvokjed', 'minsjed', 'mlokjed',
#                   'mnommno', 'mgenmno', 'mdatmno', 'makumno', 'mvokmno', 'minsmno', 'mlokmno',
#                   'znomjed', 'zgenjed', 'zdatjed', 'zakujed', 'zvokjed', 'zinsjed', 'zlokjed',
#                   'znommno', 'zgenmno', 'zdatmno', 'zakumno', 'zvokmno', 'zinsmno', 'zlokmno',
#                   'snomjed', 'sgenjed', 'sdatjed', 'sakujed', 'svokjed', 'sinsjed', 'slokjed',
#                   'snommno', 'sgenmno', 'sdatmno', 'sakumno', 'svokmno', 'sinsmno', 'slokmno')


class PridevSerializer(serializers.ModelSerializer):
    # vidprideva_set = VidPridevaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Pridev
        fields = ['id', 'recnik_id', 'status', 'vreme_kreiranja', 'poslednja_izmena', 
                  'osnovni_oblik', 'vrsta_reci', 'naziv_vrste_reci', 'vlasnik', 'dva_vida',
                  'monomjed', 'mogenjed',  'modatjed',  'moakujed',  'movokjed',  'moinsjed',  'molokjed',  
                  'monommno',  'mogenmno',  'modatmno',  'moakumno',  'movokmno',  'moinsmno',  'molokmno',  
                  'mnnomjed',  'mngenjed',  'mndatjed',  'mnakujed',  'mnvokjed',  'mninsjed',  'mnlokjed',  
                  'mnnommno',  'mngenmno',  'mndatmno',  'mnakumno',  'mnvokmno',  'mninsmno',  'mnlokmno',  
                  'mknomjed',  'mkgenjed',  'mkdatjed',  'mkakujed',  'mkvokjed',  'mkinsjed',  'mklokjed',  
                  'mknommno',  'mkgenmno',  'mkdatmno',  'mkakumno',  'mkvokmno',  'mkinsmno',  'mklokmno',  
                  'msnomjed',  'msgenjed',  'msdatjed',  'msakujed',  'msvokjed',  'msinsjed',  'mslokjed',  
                  'msnommno',  'msgenmno',  'msdatmno',  'msakumno',  'msvokmno',  'msinsmno',  'mslokmno',  
                  'zpnomjed',  'zpgenjed',  'zpdatjed',  'zpakujed',  'zpvokjed',  'zpinsjed',  'zplokjed',  
                  'zpnommno',  'zpgenmno',  'zpdatmno',  'zpakumno',  'zpvokmno',  'zpinsmno',  'zplokmno',  
                  'zknomjed',  'zkgenjed',  'zkdatjed',  'zkakujed',  'zkvokjed',  'zkinsjed',  'zklokjed',  
                  'zknommno',  'zkgenmno',  'zkdatmno',  'zkakumno',  'zkvokmno',  'zkinsmno',  'zklokmno',  
                  'zsnomjed',  'zsgenjed',  'zsdatjed',  'zsakujed',  'zsvokjed',  'zsinsjed',  'zslokjed',  
                  'zsnommno',  'zsgenmno',  'zsdatmno',  'zsakumno',  'zsvokmno',  'zsinsmno',  'zslokmno',  
                  'spnomjed',  'spgenjed',  'spdatjed',  'spakujed',  'spvokjed',  'spinsjed',  'splokjed',  
                  'spnommno',  'spgenmno',  'spdatmno',  'spakumno',  'spvokmno',  'spinsmno',  'splokmno',  
                  'sknomjed',  'skgenjed',  'skdatjed',  'skakujed',  'skvokjed',  'skinsjed',  'sklokjed',  
                  'sknommno',  'skgenmno',  'skdatmno',  'skakumno',  'skvokmno',  'skinsmno',  'sklokmno',  
                  'ssnomjed',  'ssgenjed',  'ssdatjed',  'ssakujed',  'ssvokjed',  'ssinsjed',  'sslokjed',  
                  'ssnommno',  'ssgenmno',  'ssdatmno',  'ssakumno',  'ssvokmno',  'ssinsmno',  'sslokmno']


class IzmenaPredlogaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IzmenaPredloga
        fields = ('id', 'operacija_izmene', 'user', 'vreme')


class PredlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predlog
        fields = ('id', 'tekst', 'vreme_kreiranja', 'poslednja_izmena', 'osnovni_oblik', 'vrsta_reci', 'naziv_vrste_reci', 'vlasnik')


class IzmenaRecceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IzmenaRecce
        fields = ('id', 'operacija_izmene', 'user', 'vreme')


class ReccaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recca
        fields = ('id', 'tekst', 'vreme_kreiranja', 'poslednja_izmena', 'osnovni_oblik', 'vrsta_reci', 'naziv_vrste_reci', 'vlasnik')
        

class IzmenaUzvikaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IzmenaUzvika
        fields = ('id', 'operacija_izmene', 'user', 'vreme')


class UzvikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uzvik
        fields = ('id', 'tekst', 'vreme_kreiranja', 'poslednja_izmena', 'osnovni_oblik', 'vrsta_reci', 'naziv_vrste_reci', 'vlasnik')
        

class IzmenaVeznikaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IzmenaVeznika
        fields = ('id', 'operacija_izmene', 'user', 'vreme')


class VeznikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veznik
        fields = ('id', 'tekst', 'vreme_kreiranja', 'poslednja_izmena', 'osnovni_oblik', 'vrsta_reci', 'naziv_vrste_reci', 'vlasnik')
        

class VarijantaZameniceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VarijantaZamenice
        fields = ('id', 'redni_broj', 'nomjed', 'genjed', 'datjed', 'akujed', 'vokjed', 'insjed', 'lokjed')


class ZamenicaSerializer(serializers.ModelSerializer):
    varijantazamenice_set = VarijantaZameniceSerializer(many=True, read_only=True)

    class Meta:
        model = Zamenica
        fields = ('id', 'nomjed', 'genjed', 'datjed', 'akujed', 'vokjed', 'insjed', 'lokjed', 'varijantazamenice_set',
                  'vreme_kreiranja', 'poslednja_izmena', 'osnovni_oblik', 'vrsta_reci', 'naziv_vrste_reci', 'vlasnik')
        

class BrojSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broj
        fields = ('id', 'nomjed', 'genjed', 'datjed', 'akujed', 'vokjed', 'insjed', 'lokjed', 
                  'nommno', 'genmno', 'datmno', 'akumno', 'vokmno', 'insmno', 'lokmno', 
                  'vreme_kreiranja', 'poslednja_izmena', 'osnovni_oblik', 'vrsta_reci', 'naziv_vrste_reci', 'vlasnik')
        

class PrilogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prilog
        fields = ('id', 'komparativ', 'superlativ', 'vreme_kreiranja', 'poslednja_izmena', 'osnovni_oblik', 'vrsta_reci', 'naziv_vrste_reci', 'vlasnik')
        

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
        validated_data['vlasnik'] = user
        imenica, created = Imenica.objects.update_or_create(defaults=validated_data, id=imenica_id)
        VarijantaImenice.objects.filter(imenica=imenica).delete()
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
        validated_data['vlasnik'] = user
        glagol, created = Glagol.objects.update_or_create(defaults=validated_data, id=glagol_id)
        OblikGlagola.objects.filter(glagol=glagol).delete()
        for oblik in oblici:
            varijante = oblik.pop('varijante', [])
            oblik = OblikGlagola.objects.create(glagol=glagol, **oblik)
            for var in varijante:
                VarijanteGlagola.objects.create(oblik_glagola=oblik, **var)
        operacija_izmene = 2 if radimo_update else 1
        IzmenaGlagola.objects.create(user_id=user.id, vreme=sada, glagol=glagol, operacija_izmene=operacija_izmene)
        return glagol


# class SaveVidPridevaSerializer(NoSaveSerializer):
#     vid = serializers.IntegerField(required=False)
#     mnomjed = serializers.CharField(max_length=25, allow_blank=True)
#     mgenjed = serializers.CharField(max_length=25, allow_blank=True)
#     mdatjed = serializers.CharField(max_length=25, allow_blank=True)
#     makujed = serializers.CharField(max_length=25, allow_blank=True)
#     mvokjed = serializers.CharField(max_length=25, allow_blank=True)
#     minsjed = serializers.CharField(max_length=25, allow_blank=True)
#     mlokjed = serializers.CharField(max_length=25, allow_blank=True)
#     mnommno = serializers.CharField(max_length=25, allow_blank=True)
#     mgenmno = serializers.CharField(max_length=25, allow_blank=True)
#     mdatmno = serializers.CharField(max_length=25, allow_blank=True)
#     makumno = serializers.CharField(max_length=25, allow_blank=True)
#     mvokmno = serializers.CharField(max_length=25, allow_blank=True)
#     minsmno = serializers.CharField(max_length=25, allow_blank=True)
#     mlokmno = serializers.CharField(max_length=25, allow_blank=True)
#     znomjed = serializers.CharField(max_length=25, allow_blank=True)
#     zgenjed = serializers.CharField(max_length=25, allow_blank=True)
#     zdatjed = serializers.CharField(max_length=25, allow_blank=True)
#     zakujed = serializers.CharField(max_length=25, allow_blank=True)
#     zvokjed = serializers.CharField(max_length=25, allow_blank=True)
#     zinsjed = serializers.CharField(max_length=25, allow_blank=True)
#     zlokjed = serializers.CharField(max_length=25, allow_blank=True)
#     znommno = serializers.CharField(max_length=25, allow_blank=True)
#     zgenmno = serializers.CharField(max_length=25, allow_blank=True)
#     zdatmno = serializers.CharField(max_length=25, allow_blank=True)
#     zakumno = serializers.CharField(max_length=25, allow_blank=True)
#     zvokmno = serializers.CharField(max_length=25, allow_blank=True)
#     zinsmno = serializers.CharField(max_length=25, allow_blank=True)
#     zlokmno = serializers.CharField(max_length=25, allow_blank=True)
#     snomjed = serializers.CharField(max_length=25, allow_blank=True)
#     sgenjed = serializers.CharField(max_length=25, allow_blank=True)
#     sdatjed = serializers.CharField(max_length=25, allow_blank=True)
#     sakujed = serializers.CharField(max_length=25, allow_blank=True)
#     svokjed = serializers.CharField(max_length=25, allow_blank=True)
#     sinsjed = serializers.CharField(max_length=25, allow_blank=True)
#     slokjed = serializers.CharField(max_length=25, allow_blank=True)
#     snommno = serializers.CharField(max_length=25, allow_blank=True)
#     sgenmno = serializers.CharField(max_length=25, allow_blank=True)
#     sdatmno = serializers.CharField(max_length=25, allow_blank=True)
#     sakumno = serializers.CharField(max_length=25, allow_blank=True)
#     svokmno = serializers.CharField(max_length=25, allow_blank=True)
#     sinsmno = serializers.CharField(max_length=25, allow_blank=True)
#     slokmno = serializers.CharField(max_length=25, allow_blank=True)


class SavePridevSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    dvaVida = serializers.BooleanField(required=True)
    monomjed = serializers.CharField(required=True, allow_null=True)
    mogenjed = serializers.CharField(required=True, allow_null=True)
    modatjed = serializers.CharField(required=True, allow_null=True)
    moakujed = serializers.CharField(required=True, allow_null=True)
    movokjed = serializers.CharField(required=True, allow_null=True)
    moinsjed = serializers.CharField(required=True, allow_null=True)
    molokjed = serializers.CharField(required=True, allow_null=True)
    monommno = serializers.CharField(required=True, allow_null=True)
    mogenmno = serializers.CharField(required=True, allow_null=True)
    modatmno = serializers.CharField(required=True, allow_null=True)
    moakumno = serializers.CharField(required=True, allow_null=True)
    movokmno = serializers.CharField(required=True, allow_null=True)
    moinsmno = serializers.CharField(required=True, allow_null=True)
    molokmno = serializers.CharField(required=True, allow_null=True)
    mnnomjed = serializers.CharField(required=True, allow_null=True)
    mngenjed = serializers.CharField(required=True, allow_null=True)
    mndatjed = serializers.CharField(required=True, allow_null=True)
    mnakujed = serializers.CharField(required=True, allow_null=True)
    mnvokjed = serializers.CharField(required=True, allow_null=True)
    mninsjed = serializers.CharField(required=True, allow_null=True)
    mnlokjed = serializers.CharField(required=True, allow_null=True)
    mnnommno = serializers.CharField(required=True, allow_null=True)
    mngenmno = serializers.CharField(required=True, allow_null=True)
    mndatmno = serializers.CharField(required=True, allow_null=True)
    mnakumno = serializers.CharField(required=True, allow_null=True)
    mnvokmno = serializers.CharField(required=True, allow_null=True)
    mninsmno = serializers.CharField(required=True, allow_null=True)
    mnlokmno = serializers.CharField(required=True, allow_null=True)
    mknomjed = serializers.CharField(required=True, allow_null=True)
    mkgenjed = serializers.CharField(required=True, allow_null=True)
    mkdatjed = serializers.CharField(required=True, allow_null=True)
    mkakujed = serializers.CharField(required=True, allow_null=True)
    mkvokjed = serializers.CharField(required=True, allow_null=True)
    mkinsjed = serializers.CharField(required=True, allow_null=True)
    mklokjed = serializers.CharField(required=True, allow_null=True)
    mknommno = serializers.CharField(required=True, allow_null=True)
    mkgenmno = serializers.CharField(required=True, allow_null=True)
    mkdatmno = serializers.CharField(required=True, allow_null=True)
    mkakumno = serializers.CharField(required=True, allow_null=True)
    mkvokmno = serializers.CharField(required=True, allow_null=True)
    mkinsmno = serializers.CharField(required=True, allow_null=True)
    mklokmno = serializers.CharField(required=True, allow_null=True)
    msnomjed = serializers.CharField(required=True, allow_null=True)
    msgenjed = serializers.CharField(required=True, allow_null=True)
    msdatjed = serializers.CharField(required=True, allow_null=True)
    msakujed = serializers.CharField(required=True, allow_null=True)
    msvokjed = serializers.CharField(required=True, allow_null=True)
    msinsjed = serializers.CharField(required=True, allow_null=True)
    mslokjed = serializers.CharField(required=True, allow_null=True)
    msnommno = serializers.CharField(required=True, allow_null=True)
    msgenmno = serializers.CharField(required=True, allow_null=True)
    msdatmno = serializers.CharField(required=True, allow_null=True)
    msakumno = serializers.CharField(required=True, allow_null=True)
    msvokmno = serializers.CharField(required=True, allow_null=True)
    msinsmno = serializers.CharField(required=True, allow_null=True)
    mslokmno = serializers.CharField(required=True, allow_null=True)
    zpnomjed = serializers.CharField(required=True, allow_null=True)
    zpgenjed = serializers.CharField(required=True, allow_null=True)
    zpdatjed = serializers.CharField(required=True, allow_null=True)
    zpakujed = serializers.CharField(required=True, allow_null=True)
    zpvokjed = serializers.CharField(required=True, allow_null=True)
    zpinsjed = serializers.CharField(required=True, allow_null=True)
    zplokjed = serializers.CharField(required=True, allow_null=True)
    zpnommno = serializers.CharField(required=True, allow_null=True)
    zpgenmno = serializers.CharField(required=True, allow_null=True)
    zpdatmno = serializers.CharField(required=True, allow_null=True)
    zpakumno = serializers.CharField(required=True, allow_null=True)
    zpvokmno = serializers.CharField(required=True, allow_null=True)
    zpinsmno = serializers.CharField(required=True, allow_null=True)
    zplokmno = serializers.CharField(required=True, allow_null=True)
    zknomjed = serializers.CharField(required=True, allow_null=True)
    zkgenjed = serializers.CharField(required=True, allow_null=True)
    zkdatjed = serializers.CharField(required=True, allow_null=True)
    zkakujed = serializers.CharField(required=True, allow_null=True)
    zkvokjed = serializers.CharField(required=True, allow_null=True)
    zkinsjed = serializers.CharField(required=True, allow_null=True)
    zklokjed = serializers.CharField(required=True, allow_null=True)
    zknommno = serializers.CharField(required=True, allow_null=True)
    zkgenmno = serializers.CharField(required=True, allow_null=True)
    zkdatmno = serializers.CharField(required=True, allow_null=True)
    zkakumno = serializers.CharField(required=True, allow_null=True)
    zkvokmno = serializers.CharField(required=True, allow_null=True)
    zkinsmno = serializers.CharField(required=True, allow_null=True)
    zklokmno = serializers.CharField(required=True, allow_null=True)
    zsnomjed = serializers.CharField(required=True, allow_null=True)
    zsgenjed = serializers.CharField(required=True, allow_null=True)
    zsdatjed = serializers.CharField(required=True, allow_null=True)
    zsakujed = serializers.CharField(required=True, allow_null=True)
    zsvokjed = serializers.CharField(required=True, allow_null=True)
    zsinsjed = serializers.CharField(required=True, allow_null=True)
    zslokjed = serializers.CharField(required=True, allow_null=True)
    zsnommno = serializers.CharField(required=True, allow_null=True)
    zsgenmno = serializers.CharField(required=True, allow_null=True)
    zsdatmno = serializers.CharField(required=True, allow_null=True)
    zsakumno = serializers.CharField(required=True, allow_null=True)
    zsvokmno = serializers.CharField(required=True, allow_null=True)
    zsinsmno = serializers.CharField(required=True, allow_null=True)
    zslokmno = serializers.CharField(required=True, allow_null=True)
    spnomjed = serializers.CharField(required=True, allow_null=True)
    spgenjed = serializers.CharField(required=True, allow_null=True)
    spdatjed = serializers.CharField(required=True, allow_null=True)
    spakujed = serializers.CharField(required=True, allow_null=True)
    spvokjed = serializers.CharField(required=True, allow_null=True)
    spinsjed = serializers.CharField(required=True, allow_null=True)
    splokjed = serializers.CharField(required=True, allow_null=True)
    spnommno = serializers.CharField(required=True, allow_null=True)
    spgenmno = serializers.CharField(required=True, allow_null=True)
    spdatmno = serializers.CharField(required=True, allow_null=True)
    spakumno = serializers.CharField(required=True, allow_null=True)
    spvokmno = serializers.CharField(required=True, allow_null=True)
    spinsmno = serializers.CharField(required=True, allow_null=True)
    splokmno = serializers.CharField(required=True, allow_null=True)
    sknomjed = serializers.CharField(required=True, allow_null=True)
    skgenjed = serializers.CharField(required=True, allow_null=True)
    skdatjed = serializers.CharField(required=True, allow_null=True)
    skakujed = serializers.CharField(required=True, allow_null=True)
    skvokjed = serializers.CharField(required=True, allow_null=True)
    skinsjed = serializers.CharField(required=True, allow_null=True)
    sklokjed = serializers.CharField(required=True, allow_null=True)
    sknommno = serializers.CharField(required=True, allow_null=True)
    skgenmno = serializers.CharField(required=True, allow_null=True)
    skdatmno = serializers.CharField(required=True, allow_null=True)
    skakumno = serializers.CharField(required=True, allow_null=True)
    skvokmno = serializers.CharField(required=True, allow_null=True)
    skinsmno = serializers.CharField(required=True, allow_null=True)
    sklokmno = serializers.CharField(required=True, allow_null=True)
    ssnomjed = serializers.CharField(required=True, allow_null=True)
    ssgenjed = serializers.CharField(required=True, allow_null=True)
    ssdatjed = serializers.CharField(required=True, allow_null=True)
    ssakujed = serializers.CharField(required=True, allow_null=True)
    ssvokjed = serializers.CharField(required=True, allow_null=True)
    ssinsjed = serializers.CharField(required=True, allow_null=True)
    sslokjed = serializers.CharField(required=True, allow_null=True)
    ssnommno = serializers.CharField(required=True, allow_null=True)
    ssgenmno = serializers.CharField(required=True, allow_null=True)
    ssdatmno = serializers.CharField(required=True, allow_null=True)
    ssakumno = serializers.CharField(required=True, allow_null=True)
    ssvokmno = serializers.CharField(required=True, allow_null=True)
    ssinsmno = serializers.CharField(required=True, allow_null=True)
    sslokmno = serializers.CharField(required=True, allow_null=True)
    # vidovi = serializers.ListField(child=SaveVidPridevaSerializer())

    def create(self, validated_data):
        return self._save(validated_data)

    def update(self, instance, validated_data):
        # VidPrideva.objects.filter(pridev_id=instance.id).delete()
        return self._save(validated_data, instance)

    def _save(self, validated_data, pridev=None):
        radimo_update = pridev is not None
        pridev_id = validated_data.get('id')
        sada = now()
        # vidovi = validated_data.pop('vidovi', [])
        user = validated_data.pop('user')
        dva_vida = validated_data.pop('dvaVida', True)
        validated_data['dva_vida'] = dva_vida
        validated_data['poslednja_izmena'] = sada
        validated_data['vlasnik'] = user
        pridev, created = Pridev.objects.update_or_create(defaults=validated_data, id=pridev_id)
        # VidPrideva.objects.filter(pridev=pridev).delete()
        # for v in vidovi:
        #     VidPrideva.objects.create(pridev=pridev, **v)
        if not pridev.lema:
            pridev.lema = pridev.prvi_popunjen_oblik()
            pridev.save()
        operacija_izmene = 2 if radimo_update else 1
        IzmenaPrideva.objects.create(user_id=user.id, vreme=sada, pridev=pridev, operacija_izmene=operacija_izmene)
        return pridev


class SavePredlogSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    tekst = serializers.CharField(max_length=100, allow_blank=False)

    def create(self, validated_data):
        return self._save(validated_data)

    def update(self, instance, validated_data):
        return self._save(validated_data, instance)

    def _save(self, validated_data, predlog=None):
        radimo_update = predlog is not None
        predlog_id = validated_data.get('id')
        sada = now()
        user = validated_data.pop('user')
        validated_data['poslednja_izmena'] = sada
        validated_data['vlasnik'] = user
        predlog, created = Predlog.objects.update_or_create(defaults=validated_data, id=predlog_id)
        operacija_izmene = 2 if radimo_update else 1
        IzmenaPredloga.objects.create(user_id=user.id, vreme=sada, predlog=predlog, operacija_izmene=operacija_izmene)
        return predlog


class SaveReccaSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    tekst = serializers.CharField(max_length=100, allow_blank=False)

    def create(self, validated_data):
        return self._save(validated_data)

    def update(self, instance, validated_data):
        return self._save(validated_data, instance)

    def _save(self, validated_data, recca=None):
        radimo_update = recca is not None
        recca_id = validated_data.get('id')
        sada = now()
        user = validated_data.pop('user')
        validated_data['poslednja_izmena'] = sada
        validated_data['vlasnik'] = user
        recca, created = Recca.objects.update_or_create(defaults=validated_data, id=recca_id)
        operacija_izmene = 2 if radimo_update else 1
        IzmenaRecce.objects.create(user_id=user.id, vreme=sada, recca=recca, operacija_izmene=operacija_izmene)
        return recca


class SaveUzvikSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    tekst = serializers.CharField(max_length=100, allow_blank=False)

    def create(self, validated_data):
        return self._save(validated_data)

    def update(self, instance, validated_data):
        return self._save(validated_data, instance)

    def _save(self, validated_data, uzvik=None):
        radimo_update = uzvik is not None
        uzvik_id = validated_data.get('id')
        sada = now()
        user = validated_data.pop('user')
        validated_data['poslednja_izmena'] = sada
        validated_data['vlasnik'] = user
        uzvik, created = Uzvik.objects.update_or_create(defaults=validated_data, id=uzvik_id)
        operacija_izmene = 2 if radimo_update else 1
        IzmenaUzvika.objects.create(user_id=user.id, vreme=sada, uzvik=uzvik, operacija_izmene=operacija_izmene)
        return uzvik


class SaveVeznikSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    tekst = serializers.CharField(max_length=100, allow_blank=False)

    def create(self, validated_data):
        return self._save(validated_data)

    def update(self, instance, validated_data):
        return self._save(validated_data, instance)

    def _save(self, validated_data, veznik=None):
        radimo_update = veznik is not None
        veznik_id = validated_data.get('id')
        sada = now()
        user = validated_data.pop('user')
        validated_data['poslednja_izmena'] = sada
        validated_data['vlasnik'] = user
        veznik, created = Veznik.objects.update_or_create(defaults=validated_data, id=veznik_id)
        operacija_izmene = 2 if radimo_update else 1
        IzmenaVeznika.objects.create(user_id=user.id, vreme=sada, veznik=veznik, operacija_izmene=operacija_izmene)
        return veznik


class SavePrilogSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    komparativ = serializers.CharField(max_length=50, allow_blank=True)
    superlativ = serializers.CharField(max_length=50, allow_blank=True)

    def create(self, validated_data):
        return self._save(validated_data)

    def update(self, instance, validated_data):
        return self._save(validated_data, instance)

    def _save(self, validated_data, prilog=None):
        radimo_update = prilog is not None
        prilog_id = validated_data.get('id')
        sada = now()
        user = validated_data.pop('user')
        validated_data['poslednja_izmena'] = sada
        validated_data['vlasnik'] = user
        prilog, created = Prilog.objects.update_or_create(defaults=validated_data, id=prilog_id)
        operacija_izmene = 2 if radimo_update else 1
        IzmenaPriloga.objects.create(user_id=user.id, vreme=sada, prilog=prilog, operacija_izmene=operacija_izmene)
        return prilog


class SaveVarijantaZameniceSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    nomjed = serializers.CharField(max_length=50, allow_blank=True)
    genjed = serializers.CharField(max_length=50, allow_blank=True)
    datjed = serializers.CharField(max_length=50, allow_blank=True)
    akujed = serializers.CharField(max_length=50, allow_blank=True)
    vokjed = serializers.CharField(max_length=50, allow_blank=True)
    insjed = serializers.CharField(max_length=50, allow_blank=True)
    lokjed = serializers.CharField(max_length=50, allow_blank=True)


class SaveZamenicaSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    nomjed = serializers.CharField(max_length=50, allow_blank=True)
    genjed = serializers.CharField(max_length=50, allow_blank=True)
    datjed = serializers.CharField(max_length=50, allow_blank=True)
    akujed = serializers.CharField(max_length=50, allow_blank=True)
    vokjed = serializers.CharField(max_length=50, allow_blank=True)
    insjed = serializers.CharField(max_length=50, allow_blank=True)
    lokjed = serializers.CharField(max_length=50, allow_blank=True)
    varijante = serializers.ListField(child=VarijantaZameniceSerializer())

    def create(self, validated_data):
        return self._save(validated_data)

    def update(self, instance, validated_data):
        return self._save(validated_data, instance)

    def _save(self, validated_data, zamenica=None):
        radimo_update = zamenica is not None
        zamenica_id = validated_data.get('id')
        sada = now()
        varijante = validated_data.pop('varijante', [])
        user = validated_data.pop('user')
        validated_data['poslednja_izmena'] = sada
        validated_data['vlasnik'] = user
        zamenica, created = Zamenica.objects.update_or_create(defaults=validated_data, id=zamenica_id)
        VarijantaZamenice.objects.filter(zamenica=zamenica).delete()
        for var in varijante:
            VarijantaZamenice.objects.create(zamenica=zamenica, **var)
        operacija_izmene = 2 if radimo_update else 1
        IzmenaZamenice.objects.create(user_id=user.id, vreme=sada, zamenica=zamenica, operacija_izmene=operacija_izmene)
        return zamenica


class SaveBrojSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
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

    def create(self, validated_data):
        return self._save(validated_data)

    def update(self, instance, validated_data):
        return self._save(validated_data, instance)

    def _save(self, validated_data, broj=None):
        radimo_update = broj is not None
        broj_id = validated_data.get('id')
        sada = now()
        user = validated_data.pop('user')
        validated_data['poslednja_izmena'] = sada
        validated_data['vlasnik'] = user
        broj, created = Broj.objects.update_or_create(defaults=validated_data, id=broj_id)
        operacija_izmene = 2 if radimo_update else 1
        IzmenaBroja.objects.create(user_id=user.id, vreme=sada, broj=broj, operacija_izmene=operacija_izmene)
        return broj
