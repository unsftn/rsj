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


class VarijantaPridevaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VarijantaPrideva
        fields = ('id', 'rod', 'redni_broj',
                  'onomjed', 'ogenjed', 'odatjed', 'oakujed', 'ovokjed', 'oinsjed', 'olokjed',
                  'nnomjed', 'ngenjed', 'ndatjed', 'nakujed', 'nvokjed', 'ninsjed', 'nlokjed',
                  'pnomjed', 'pgenjed', 'pdatjed', 'pakujed', 'pvokjed', 'pinsjed', 'plokjed',
                  'knomjed', 'kgenjed', 'kdatjed', 'kakujed', 'kvokjed', 'kinsjed', 'klokjed',
                  'snomjed', 'sgenjed', 'sdatjed', 'sakujed', 'svokjed', 'sinsjed', 'slokjed')


class PridevSerializer(serializers.ModelSerializer):
    varijantaprideva_set = VarijantaPridevaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Pridev
        fields = ['id', 'recnik_id', 'status', 'vreme_kreiranja', 'poslednja_izmena', 'varijantaprideva_set',
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


class SaveVarijantaPridevaSerializer(NoSaveSerializer):
    rod = serializers.IntegerField()
    redni_broj = serializers.IntegerField()
    onomjed = serializers.CharField(allow_blank=True, allow_null=True)
    ogenjed = serializers.CharField(allow_blank=True, allow_null=True)
    odatjed = serializers.CharField(allow_blank=True, allow_null=True)
    oakujed = serializers.CharField(allow_blank=True, allow_null=True)
    ovokjed = serializers.CharField(allow_blank=True, allow_null=True)
    oinsjed = serializers.CharField(allow_blank=True, allow_null=True)
    olokjed = serializers.CharField(allow_blank=True, allow_null=True)
    nnomjed = serializers.CharField(allow_blank=True, allow_null=True)
    ngenjed = serializers.CharField(allow_blank=True, allow_null=True)
    ndatjed = serializers.CharField(allow_blank=True, allow_null=True)
    nakujed = serializers.CharField(allow_blank=True, allow_null=True)
    nvokjed = serializers.CharField(allow_blank=True, allow_null=True)
    ninsjed = serializers.CharField(allow_blank=True, allow_null=True)
    nlokjed = serializers.CharField(allow_blank=True, allow_null=True)
    pnomjed = serializers.CharField(allow_blank=True, allow_null=True)
    pgenjed = serializers.CharField(allow_blank=True, allow_null=True)
    pdatjed = serializers.CharField(allow_blank=True, allow_null=True)
    pakujed = serializers.CharField(allow_blank=True, allow_null=True)
    pvokjed = serializers.CharField(allow_blank=True, allow_null=True)
    pinsjed = serializers.CharField(allow_blank=True, allow_null=True)
    plokjed = serializers.CharField(allow_blank=True, allow_null=True)
    knomjed = serializers.CharField(allow_blank=True, allow_null=True)
    kgenjed = serializers.CharField(allow_blank=True, allow_null=True)
    kdatjed = serializers.CharField(allow_blank=True, allow_null=True)
    kakujed = serializers.CharField(allow_blank=True, allow_null=True)
    kvokjed = serializers.CharField(allow_blank=True, allow_null=True)
    kinsjed = serializers.CharField(allow_blank=True, allow_null=True)
    klokjed = serializers.CharField(allow_blank=True, allow_null=True)
    snomjed = serializers.CharField(allow_blank=True, allow_null=True)
    sgenjed = serializers.CharField(allow_blank=True, allow_null=True)
    sdatjed = serializers.CharField(allow_blank=True, allow_null=True)
    sakujed = serializers.CharField(allow_blank=True, allow_null=True)
    svokjed = serializers.CharField(allow_blank=True, allow_null=True)
    sinsjed = serializers.CharField(allow_blank=True, allow_null=True)
    slokjed = serializers.CharField(allow_blank=True, allow_null=True)


class SavePridevSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    dvaVida = serializers.BooleanField(required=True)
    monomjed = serializers.CharField(allow_blank=True, allow_null=True)
    mogenjed = serializers.CharField(allow_blank=True, allow_null=True)
    modatjed = serializers.CharField(allow_blank=True, allow_null=True)
    moakujed = serializers.CharField(allow_blank=True, allow_null=True)
    movokjed = serializers.CharField(allow_blank=True, allow_null=True)
    moinsjed = serializers.CharField(allow_blank=True, allow_null=True)
    molokjed = serializers.CharField(allow_blank=True, allow_null=True)
    monommno = serializers.CharField(allow_blank=True, allow_null=True)
    mogenmno = serializers.CharField(allow_blank=True, allow_null=True)
    modatmno = serializers.CharField(allow_blank=True, allow_null=True)
    moakumno = serializers.CharField(allow_blank=True, allow_null=True)
    movokmno = serializers.CharField(allow_blank=True, allow_null=True)
    moinsmno = serializers.CharField(allow_blank=True, allow_null=True)
    molokmno = serializers.CharField(allow_blank=True, allow_null=True)
    mnnomjed = serializers.CharField(allow_blank=True, allow_null=True)
    mngenjed = serializers.CharField(allow_blank=True, allow_null=True)
    mndatjed = serializers.CharField(allow_blank=True, allow_null=True)
    mnakujed = serializers.CharField(allow_blank=True, allow_null=True)
    mnvokjed = serializers.CharField(allow_blank=True, allow_null=True)
    mninsjed = serializers.CharField(allow_blank=True, allow_null=True)
    mnlokjed = serializers.CharField(allow_blank=True, allow_null=True)
    mnnommno = serializers.CharField(allow_blank=True, allow_null=True)
    mngenmno = serializers.CharField(allow_blank=True, allow_null=True)
    mndatmno = serializers.CharField(allow_blank=True, allow_null=True)
    mnakumno = serializers.CharField(allow_blank=True, allow_null=True)
    mnvokmno = serializers.CharField(allow_blank=True, allow_null=True)
    mninsmno = serializers.CharField(allow_blank=True, allow_null=True)
    mnlokmno = serializers.CharField(allow_blank=True, allow_null=True)
    mknomjed = serializers.CharField(allow_blank=True, allow_null=True)
    mkgenjed = serializers.CharField(allow_blank=True, allow_null=True)
    mkdatjed = serializers.CharField(allow_blank=True, allow_null=True)
    mkakujed = serializers.CharField(allow_blank=True, allow_null=True)
    mkvokjed = serializers.CharField(allow_blank=True, allow_null=True)
    mkinsjed = serializers.CharField(allow_blank=True, allow_null=True)
    mklokjed = serializers.CharField(allow_blank=True, allow_null=True)
    mknommno = serializers.CharField(allow_blank=True, allow_null=True)
    mkgenmno = serializers.CharField(allow_blank=True, allow_null=True)
    mkdatmno = serializers.CharField(allow_blank=True, allow_null=True)
    mkakumno = serializers.CharField(allow_blank=True, allow_null=True)
    mkvokmno = serializers.CharField(allow_blank=True, allow_null=True)
    mkinsmno = serializers.CharField(allow_blank=True, allow_null=True)
    mklokmno = serializers.CharField(allow_blank=True, allow_null=True)
    msnomjed = serializers.CharField(allow_blank=True, allow_null=True)
    msgenjed = serializers.CharField(allow_blank=True, allow_null=True)
    msdatjed = serializers.CharField(allow_blank=True, allow_null=True)
    msakujed = serializers.CharField(allow_blank=True, allow_null=True)
    msvokjed = serializers.CharField(allow_blank=True, allow_null=True)
    msinsjed = serializers.CharField(allow_blank=True, allow_null=True)
    mslokjed = serializers.CharField(allow_blank=True, allow_null=True)
    msnommno = serializers.CharField(allow_blank=True, allow_null=True)
    msgenmno = serializers.CharField(allow_blank=True, allow_null=True)
    msdatmno = serializers.CharField(allow_blank=True, allow_null=True)
    msakumno = serializers.CharField(allow_blank=True, allow_null=True)
    msvokmno = serializers.CharField(allow_blank=True, allow_null=True)
    msinsmno = serializers.CharField(allow_blank=True, allow_null=True)
    mslokmno = serializers.CharField(allow_blank=True, allow_null=True)
    zpnomjed = serializers.CharField(allow_blank=True, allow_null=True)
    zpgenjed = serializers.CharField(allow_blank=True, allow_null=True)
    zpdatjed = serializers.CharField(allow_blank=True, allow_null=True)
    zpakujed = serializers.CharField(allow_blank=True, allow_null=True)
    zpvokjed = serializers.CharField(allow_blank=True, allow_null=True)
    zpinsjed = serializers.CharField(allow_blank=True, allow_null=True)
    zplokjed = serializers.CharField(allow_blank=True, allow_null=True)
    zpnommno = serializers.CharField(allow_blank=True, allow_null=True)
    zpgenmno = serializers.CharField(allow_blank=True, allow_null=True)
    zpdatmno = serializers.CharField(allow_blank=True, allow_null=True)
    zpakumno = serializers.CharField(allow_blank=True, allow_null=True)
    zpvokmno = serializers.CharField(allow_blank=True, allow_null=True)
    zpinsmno = serializers.CharField(allow_blank=True, allow_null=True)
    zplokmno = serializers.CharField(allow_blank=True, allow_null=True)
    zknomjed = serializers.CharField(allow_blank=True, allow_null=True)
    zkgenjed = serializers.CharField(allow_blank=True, allow_null=True)
    zkdatjed = serializers.CharField(allow_blank=True, allow_null=True)
    zkakujed = serializers.CharField(allow_blank=True, allow_null=True)
    zkvokjed = serializers.CharField(allow_blank=True, allow_null=True)
    zkinsjed = serializers.CharField(allow_blank=True, allow_null=True)
    zklokjed = serializers.CharField(allow_blank=True, allow_null=True)
    zknommno = serializers.CharField(allow_blank=True, allow_null=True)
    zkgenmno = serializers.CharField(allow_blank=True, allow_null=True)
    zkdatmno = serializers.CharField(allow_blank=True, allow_null=True)
    zkakumno = serializers.CharField(allow_blank=True, allow_null=True)
    zkvokmno = serializers.CharField(allow_blank=True, allow_null=True)
    zkinsmno = serializers.CharField(allow_blank=True, allow_null=True)
    zklokmno = serializers.CharField(allow_blank=True, allow_null=True)
    zsnomjed = serializers.CharField(allow_blank=True, allow_null=True)
    zsgenjed = serializers.CharField(allow_blank=True, allow_null=True)
    zsdatjed = serializers.CharField(allow_blank=True, allow_null=True)
    zsakujed = serializers.CharField(allow_blank=True, allow_null=True)
    zsvokjed = serializers.CharField(allow_blank=True, allow_null=True)
    zsinsjed = serializers.CharField(allow_blank=True, allow_null=True)
    zslokjed = serializers.CharField(allow_blank=True, allow_null=True)
    zsnommno = serializers.CharField(allow_blank=True, allow_null=True)
    zsgenmno = serializers.CharField(allow_blank=True, allow_null=True)
    zsdatmno = serializers.CharField(allow_blank=True, allow_null=True)
    zsakumno = serializers.CharField(allow_blank=True, allow_null=True)
    zsvokmno = serializers.CharField(allow_blank=True, allow_null=True)
    zsinsmno = serializers.CharField(allow_blank=True, allow_null=True)
    zslokmno = serializers.CharField(allow_blank=True, allow_null=True)
    spnomjed = serializers.CharField(allow_blank=True, allow_null=True)
    spgenjed = serializers.CharField(allow_blank=True, allow_null=True)
    spdatjed = serializers.CharField(allow_blank=True, allow_null=True)
    spakujed = serializers.CharField(allow_blank=True, allow_null=True)
    spvokjed = serializers.CharField(allow_blank=True, allow_null=True)
    spinsjed = serializers.CharField(allow_blank=True, allow_null=True)
    splokjed = serializers.CharField(allow_blank=True, allow_null=True)
    spnommno = serializers.CharField(allow_blank=True, allow_null=True)
    spgenmno = serializers.CharField(allow_blank=True, allow_null=True)
    spdatmno = serializers.CharField(allow_blank=True, allow_null=True)
    spakumno = serializers.CharField(allow_blank=True, allow_null=True)
    spvokmno = serializers.CharField(allow_blank=True, allow_null=True)
    spinsmno = serializers.CharField(allow_blank=True, allow_null=True)
    splokmno = serializers.CharField(allow_blank=True, allow_null=True)
    sknomjed = serializers.CharField(allow_blank=True, allow_null=True)
    skgenjed = serializers.CharField(allow_blank=True, allow_null=True)
    skdatjed = serializers.CharField(allow_blank=True, allow_null=True)
    skakujed = serializers.CharField(allow_blank=True, allow_null=True)
    skvokjed = serializers.CharField(allow_blank=True, allow_null=True)
    skinsjed = serializers.CharField(allow_blank=True, allow_null=True)
    sklokjed = serializers.CharField(allow_blank=True, allow_null=True)
    sknommno = serializers.CharField(allow_blank=True, allow_null=True)
    skgenmno = serializers.CharField(allow_blank=True, allow_null=True)
    skdatmno = serializers.CharField(allow_blank=True, allow_null=True)
    skakumno = serializers.CharField(allow_blank=True, allow_null=True)
    skvokmno = serializers.CharField(allow_blank=True, allow_null=True)
    skinsmno = serializers.CharField(allow_blank=True, allow_null=True)
    sklokmno = serializers.CharField(allow_blank=True, allow_null=True)
    ssnomjed = serializers.CharField(allow_blank=True, allow_null=True)
    ssgenjed = serializers.CharField(allow_blank=True, allow_null=True)
    ssdatjed = serializers.CharField(allow_blank=True, allow_null=True)
    ssakujed = serializers.CharField(allow_blank=True, allow_null=True)
    ssvokjed = serializers.CharField(allow_blank=True, allow_null=True)
    ssinsjed = serializers.CharField(allow_blank=True, allow_null=True)
    sslokjed = serializers.CharField(allow_blank=True, allow_null=True)
    ssnommno = serializers.CharField(allow_blank=True, allow_null=True)
    ssgenmno = serializers.CharField(allow_blank=True, allow_null=True)
    ssdatmno = serializers.CharField(allow_blank=True, allow_null=True)
    ssakumno = serializers.CharField(allow_blank=True, allow_null=True)
    ssvokmno = serializers.CharField(allow_blank=True, allow_null=True)
    ssinsmno = serializers.CharField(allow_blank=True, allow_null=True)
    sslokmno = serializers.CharField(allow_blank=True, allow_null=True)
    varijante = serializers.ListField(child=SaveVarijantaPridevaSerializer())

    def create(self, validated_data):
        return self._save(validated_data)

    def update(self, instance, validated_data):
        VarijantaPrideva.objects.filter(pridev_id=instance.id).delete()
        return self._save(validated_data, instance)

    def _save(self, validated_data, pridev=None):
        radimo_update = pridev is not None
        pridev_id = validated_data.get('id')
        sada = now()
        varijante = validated_data.pop('varijante', [])
        user = validated_data.pop('user')
        dva_vida = validated_data.pop('dvaVida', True)
        validated_data['dva_vida'] = dva_vida
        validated_data['poslednja_izmena'] = sada
        validated_data['vlasnik'] = user
        pridev, created = Pridev.objects.update_or_create(defaults=validated_data, id=pridev_id)
        VarijantaPrideva.objects.filter(pridev=pridev).delete()
        for i, v in enumerate(varijante):
            v['redni_broj'] = i + 1
            VarijantaPrideva.objects.create(pridev=pridev, **v)
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
