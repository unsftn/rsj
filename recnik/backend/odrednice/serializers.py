import logging
from django.forms.models import model_to_dict
from rest_framework import serializers
from publikacije.models import Publikacija
from .models import *
from django.contrib.auth.models import User

log = logging.getLogger(__name__)


# read-only serializers

class KvalifikatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kvalifikator
        fields = ('id', 'skracenica', 'naziv')


class KvalifikatorOdredniceSerializer(serializers.ModelSerializer):
    class Meta:
        model = KvalifikatorOdrednice
        fields = ('redni_broj', 'kvalifikator_id', 'odrednica_id',)


class KvalifikatorZnacenjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = KvalifikatorZnacenja
        fields = ('redni_broj', 'kvalifikator_id', 'znacenje_id',)


class KvalifikatorPodznacenjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = KvalifikatorPodznacenja
        fields = ('redni_broj', 'kvalifikator_id', 'podznacenje_id',)


class AntonimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Antonim
        fields = ('id', 'redni_broj', 'ima_antonim_id', 'u_vezi_sa_id', 'tekst')


class SinonimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sinonim
        fields = ('id', 'redni_broj', 'ima_sinonim_id', 'u_vezi_sa_id', 'tekst')


class RecUKolokacijiSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecUKolokaciji
        fields = ('id', 'redni_broj', 'kolokacija_id', 'odrednica_id', 'tekst')


class KolokacijaSerializer(serializers.ModelSerializer):
    recukolokaciji_set = RecUKolokacijiSerializer(many=True, required=False)

    class Meta:
        model = Kolokacija
        fields = ('id', 'napomena', 'odrednica_id', 'redni_broj', 'recukolokaciji_set')


class KvalifikatorFrazeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KvalifikatorFraze
        fields = ('redni_broj', 'kvalifikator_id', 'izrazfraza_id',)


class IzrazFrazaSerializer(serializers.ModelSerializer):
    kvalifikatorfraze_set = KvalifikatorFrazeSerializer(many=True)

    class Meta:
        model = IzrazFraza
        fields = ('id', 'opis', 'tekst', 'redni_broj', 'odrednica_id', 'znacenje_id', 'podznacenje_id',
                  'kvalifikatorfraze_set', 'vezana_odrednica_id')


class KonkordansaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Konkordansa
        fields = ('id', 'redni_broj', 'opis', 'znacenje_id', 'podznacenje_id', 'publikacija_id')


class KolokacijaZnacenjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = KolokacijaZnacenja
        fields = ('id', 'redni_broj', 'znacenje_id', 'tekst')


class KolokacijaPodznacenjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = KolokacijaPodznacenja
        fields = ('id', 'redni_broj', 'podznacenje_id', 'tekst')


class PodznacenjeSerializer(serializers.ModelSerializer):
    kvalifikatorpodznacenja_set = KvalifikatorPodznacenjaSerializer(many=True)
    izrazfraza_set = IzrazFrazaSerializer(many=True, read_only=True)
    konkordansa_set = KonkordansaSerializer(many=True, read_only=True)
    kolokacijapodznacenja_set = KolokacijaPodznacenjaSerializer(many=True, read_only=True)

    class Meta:
        model = Podznacenje
        fields = ('id', 'tekst', 'znacenje_id', 'redni_broj', 'kvalifikatorpodznacenja_set', 'izrazfraza_set',
                  'konkordansa_set', 'kolokacijapodznacenja_set')


class ZnacenjeSerializer(serializers.ModelSerializer):
    podznacenje_set = PodznacenjeSerializer(many=True, read_only=True)
    kvalifikatorznacenja_set = KvalifikatorZnacenjaSerializer(many=True)
    izrazfraza_set = IzrazFrazaSerializer(many=True, read_only=True)
    konkordansa_set = KonkordansaSerializer(many=True, read_only=True)
    kolokacijaznacenja_set = KolokacijaZnacenjaSerializer(many=True, read_only=True)

    class Meta:
        model = Znacenje
        fields = ('id', 'tekst', 'znacenje_se', 'odrednica_id', 'podznacenje_set', 'kvalifikatorznacenja_set',
                  'izrazfraza_set', 'konkordansa_set', 'redni_broj', 'kolokacijaznacenja_set')


class UserSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()

    def get_group(self, obj):
        return obj.group_id()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'group')


class OperacijaIzmeneSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperacijaIzmene
        fields = ('id', 'naziv')


class IzmenaOdredniceSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    operacija_izmene = OperacijaIzmeneSerializer()

    class Meta:
        model = IzmenaOdrednice
        fields = ('id', 'odrednica_id', 'operacija_izmene', 'user', 'vreme')


class VarijantaOdredniceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VarijantaOdrednice
        fields = ('id', 'redni_broj', 'tekst', 'ijekavski', 'nastavak', 'nastavak_ij', 'prezent', 'prezent_ij',
                  'opciono_se')


class StatusOdredniceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusOdrednice
        fields = ('id', 'naziv')


class OdrednicaSerializer(serializers.ModelSerializer):
    ima_antonim = AntonimSerializer(many=True, read_only=True)
    ima_sinonim = SinonimSerializer(many=True, read_only=True)
    kolokacija_set = KolokacijaSerializer(many=True, read_only=True)
    znacenje_set = ZnacenjeSerializer(many=True, read_only=True)
    izrazfraza_set = IzrazFrazaSerializer(many=True, read_only=True)
    varijantaodrednice_set = VarijantaOdredniceSerializer(many=True, read_only=True)
    kvalifikatorodrednice_set = KvalifikatorOdredniceSerializer(many=True, read_only=True)
    izmenaodrednice_set = IzmenaOdredniceSerializer(many=True, read_only=True)

    class Meta:
        model = Odrednica
        fields = ('id', 'rec', 'ijekavski', 'vrsta', 'rod', 'nastavak', 'nastavak_ij', 'info', 'glagolski_vid',
                  'glagolski_rod', 'prezent', 'prezent_ij', 'broj_pregleda', 'vreme_kreiranja', 'poslednja_izmena',
                  'stanje', 'version', 'varijantaodrednice_set', 'ima_antonim', 'ima_sinonim',
                  'kolokacija_set', 'znacenje_set', 'izrazfraza_set', 'kvalifikatorodrednice_set',
                  'izmenaodrednice_set', 'opciono_se', 'rbr_homonima', 'obradjivac', 'redaktor', 'urednik', 'napomene',
                  'freetext', 'status')


class ShortOdrednicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Odrednica
        fields = ('id', 'rec', 'vrsta', 'vreme_kreiranja', 'poslednja_izmena', 'stanje', 'obradjivac', 'redaktor',
                  'urednik', 'status')


# insert/update serializers

class NoSaveSerializer(serializers.Serializer):
    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        return instance


class CreateUpdateIzrazFrazaSerializer(NoSaveSerializer):
    pass


class CreateKvalifikatorOdredniceSerializer(NoSaveSerializer):
    pass


class CreatePojavaKvalifikatoraSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    kvalifikator_id = serializers.IntegerField()


class CreateIzmenaOdredniceSerializer(NoSaveSerializer):
    vreme = serializers.DateTimeField()
    user_id = serializers.IntegerField()
    operacija_izmene_id = serializers.IntegerField()


class CreateUpdateOperacijaIzmeneSerializer(NoSaveSerializer):
    pass


class CreateRecUKolokacijiSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    odrednica_id = serializers.IntegerField(allow_null=True)
    tekst = serializers.CharField(allow_null=True, allow_blank=True, required=False)


class CreateKolokacijaSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    odrednice = serializers.ListSerializer(child=CreateRecUKolokacijiSerializer(), required=False)
    napomena = serializers.CharField(max_length=2000, required=True, allow_null=True, allow_blank=True)


class CreateIzrazFrazaSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    opis = serializers.CharField(max_length=2000, allow_blank=True)
    tekst = serializers.CharField(max_length=200, required=False, allow_blank=True)
    kvalifikatori = serializers.ListField(child=CreatePojavaKvalifikatoraSerializer(), required=False)
    vezana_odrednica_id = serializers.IntegerField(required=False, allow_null=True)


class CreateKonkordansaSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    opis = serializers.CharField(max_length=2000, allow_blank=True)
    publikacija_id = serializers.IntegerField(required=False, allow_null=True)


class CreateKolokacijaPodznacenjaSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    tekst = serializers.CharField(max_length=2000, required=False, allow_blank=True)


class CreatePodznacenjeSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    tekst = serializers.CharField(max_length=2000, required=False, allow_blank=True)
    kvalifikatori = serializers.ListField(child=CreatePojavaKvalifikatoraSerializer(), required=False)
    izrazi_fraze = serializers.ListField(child=CreateIzrazFrazaSerializer(), required=False)
    konkordanse = serializers.ListField(child=CreateKonkordansaSerializer(), required=False)
    kolokacije = serializers.ListSerializer(child=CreateKolokacijaPodznacenjaSerializer(), required=False)


class CreateKolokacijaZnacenjaSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    tekst = serializers.CharField(max_length=2000, required=False, allow_blank=True)


class CreateZnacenjeSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    tekst = serializers.CharField(max_length=2000, required=False, allow_blank=True)
    znacenje_se = serializers.BooleanField()
    podznacenja = serializers.ListField(child=CreatePodznacenjeSerializer(), required=False)
    kvalifikatori = serializers.ListField(child=CreatePojavaKvalifikatoraSerializer(), required=False)
    izrazi_fraze = serializers.ListField(child=CreateIzrazFrazaSerializer(), required=False)
    konkordanse = serializers.ListField(child=CreateKonkordansaSerializer(), required=False)
    kolokacije = serializers.ListSerializer(child=CreateKolokacijaZnacenjaSerializer(), required=False)


class CreateSinonimSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    sinonim_id = serializers.IntegerField(allow_null=True)
    tekst = serializers.CharField(allow_null=True, allow_blank=True, required=False)


class CreateAntonimSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    antonim_id = serializers.IntegerField(allow_null=True)
    tekst = serializers.CharField(allow_null=True, allow_blank=True, required=False)


class CreateVarijantaOdredniceSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    tekst = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    ijekavski = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    nastavak = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    nastavak_ij = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    prezent = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    prezent_ij = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    opciono_se = serializers.NullBooleanField(required=False)


class CreateOdrednicaSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    rec = serializers.CharField(max_length=50)
    ijekavski = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    vrsta = serializers.IntegerField(required=False)
    rod = serializers.IntegerField(required=False, allow_null=True)
    nastavak = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    nastavak_ij = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    info = serializers.CharField(max_length=2000, required=False, allow_blank=True, allow_null=True)
    glagolski_vid = serializers.IntegerField(required=False, allow_null=True)
    glagolski_rod = serializers.IntegerField(required=False, allow_null=True)
    prezent = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    prezent_ij = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    stanje = serializers.IntegerField(required=False, allow_null=True)
    version = serializers.IntegerField(required=False, allow_null=True)
    opciono_se = serializers.NullBooleanField(required=False)
    napomene = serializers.CharField(max_length=2000, required=False, allow_blank=True, allow_null=True)
    freetext = serializers.CharField(max_length=2000, required=False, allow_blank=True, allow_null=True)
    znacenja = serializers.ListField(child=CreateZnacenjeSerializer())
    kvalifikatori = serializers.ListField(child=CreatePojavaKvalifikatoraSerializer(), required=False)
    varijante = serializers.ListField(child=CreateVarijantaOdredniceSerializer(), required=False)
    izrazi_fraze = serializers.ListField(child=CreateIzrazFrazaSerializer(), required=False)
    sinonimi = serializers.ListField(child=CreateSinonimSerializer(), required=False)
    antonimi = serializers.ListField(child=CreateAntonimSerializer(), required=False)
    rbr_homonima = serializers.IntegerField(required=False, allow_null=True)
    kolokacije = serializers.ListField(child=CreateKolokacijaSerializer(), required=False)
    status_id = serializers.IntegerField(required=False, allow_null=True)

    def instantiate(self):
        return self._save(self.validated_data, None, 'memory')

    def create(self, validated_data):
        return self._save(validated_data)

    def update(self, instance, validated_data):
        Znacenje.objects.filter(odrednica_id=instance.id).delete()
        IzrazFraza.objects.filter(odrednica_id=instance.id).delete()
        KvalifikatorOdrednice.objects.filter(odrednica_id=instance.id).delete()
        VarijantaOdrednice.objects.filter(odrednica_id=instance.id).delete()
        Kolokacija.objects.filter(odrednica_id=instance.id).delete()
        Antonim.objects.filter(ima_antonim_id=instance.id).delete()
        Sinonim.objects.filter(ima_sinonim_id=instance.id).delete()

        return self._save(validated_data, instance)

    def _save(self, validated_data, odrednica=None, database='default'):
        radimo_update = odrednica is not None
        user = validated_data.pop('user') if database == 'default' else None

        odrednica_id = validated_data.get('id')

        sada = now()
        znacenja = validated_data.pop('znacenja', [])
        kvalifikatori_odrednice = validated_data.pop('kvalifikatori', [])
        varijante = validated_data.pop('varijante', [])
        izrazi_fraze = validated_data.pop('izrazi_fraze', [])
        sinonimi = validated_data.pop('sinonimi', [])
        antonimi = validated_data.pop('antonimi', [])
        kolokacije = validated_data.pop('kolokacije', [])

        validated_data['poslednja_izmena'] = sada
        if database == 'default':
            if validated_data['stanje'] == 1:
                validated_data['obradjivac'] = user
            elif validated_data['stanje'] == 2:
                validated_data['redaktor'] = user
            elif validated_data['stanje'] == 3:
                validated_data['urednik'] = user
        odrednica, created = Odrednica.objects.using(database).update_or_create(defaults=validated_data, id=odrednica_id)

        for var_odr in varijante:
            VarijantaOdrednice.objects.using(database).create(odrednica=odrednica, **var_odr)
        for kvod in kvalifikatori_odrednice:
            KvalifikatorOdrednice.objects.using(database).create(odrednica=odrednica, **kvod)
        for izr_frz in izrazi_fraze:
            kvalifikatori_fraze = izr_frz.pop('kvalifikatori', [])
            if database != 'default' and izr_frz.get('vezana_odrednica_id'):
                izr_frz['vezana_odrednica_id'] = None
            iz = IzrazFraza.objects.using(database).create(odrednica=odrednica, **izr_frz)
            for kv in kvalifikatori_fraze:
                KvalifikatorFraze.objects.using(database).create(izrazfraza=iz, **kv)
        for znacenje in znacenja:
            kvalifikatori = znacenje.pop('kvalifikatori', [])
            podznacenja = znacenje.pop('podznacenja', [])
            izrazi_fraze_znacenja = znacenje.pop('izrazi_fraze', [])
            konkordanse_znacenja = znacenje.pop('konkordanse', [])
            kolokacije_znacenja = znacenje.pop('kolokacije', [])
            z = Znacenje.objects.using(database).create(odrednica=odrednica, **znacenje)
            for k in kvalifikatori:
                KvalifikatorZnacenja.objects.using(database).create(znacenje=z, **k)
            for ifz in izrazi_fraze_znacenja:
                kvalifikatori_fraze = ifz.pop('kvalifikatori', [])
                if database != 'default' and ifz.get('vezana_odrednica_id'):
                    ifz['vezana_odrednica_id'] = None
                iz = IzrazFraza.objects.using(database).create(znacenje=z, **ifz)
                for kv in kvalifikatori_fraze:
                    KvalifikatorFraze.objects.using(database).create(izrazfraza=iz, **kv)
            for konz in konkordanse_znacenja:
                if database != 'default' and konz['publikacija_id']:
                    dst_pub = self._make_fake_pub(konz, database)
                    del konz['publikacija_id']
                    Konkordansa.objects.using(database).create(znacenje=z, publikacija=dst_pub, **konz)
                else:
                    Konkordansa.objects.using(database).create(znacenje=z, **konz)
            for kol in kolokacije_znacenja:
                KolokacijaZnacenja.objects.using(database).create(znacenje=z, **kol)
            for podz in podznacenja:
                kvalifikatori_podznacenja = podz.pop('kvalifikatori', [])
                izrazi_fraze_podznacenja = podz.pop('izrazi_fraze', [])
                konkordanse_podznacenja = podz.pop('konkordanse', [])
                kolokacije_podznacenja = podz.pop('kolokacije', [])
                p = Podznacenje.objects.using(database).create(znacenje=z, **podz)
                for k in kvalifikatori_podznacenja:
                    KvalifikatorPodznacenja.objects.using(database).create(podznacenje=p, **k)
                for ifp in izrazi_fraze_podznacenja:
                    kvalifikatori_fraze = ifp.pop('kvalifikatori', [])
                    if database != 'default' and ifp.get('vezana_odrednica_id'):
                        ifp['vezana_odrednica_id'] = None
                    iz = IzrazFraza.objects.using(database).create(podznacenje=p, **ifp)
                    for kv in kvalifikatori_fraze:
                        KvalifikatorFraze.objects.using(database).create(izrazfraza=iz, **kv)
                for konz in konkordanse_podznacenja:
                    if database != 'default' and konz['publikacija_id']:
                        dst_pub = self._make_fake_pub(konz, database)
                        del konz['publikacija_id']
                        Konkordansa.objects.using(database).create(podznacenje=p, publikacija=dst_pub, **konz)
                    else:
                        Konkordansa.objects.using(database).create(podznacenje=p, **konz)
                for kol in kolokacije_podznacenja:
                    KolokacijaPodznacenja.objects.using(database).create(podznacenje=p, **kol)
        if database == 'default':
            for kol in kolokacije:
                odrednice = kol.pop('odrednice', [])
                k = Kolokacija.objects.using(database).create(**kol, odrednica=odrednica)
                for odr in odrednice:
                    RecUKolokaciji.objects.using(database).create(kolokacija=k, **odr)
            for sin in sinonimi:
                Sinonim.objects.using(database).create(
                    redni_broj=sin['redni_broj'], u_vezi_sa_id=sin['sinonim_id'],  tekst=sin['tekst'],
                    ima_sinonim=odrednica)
            for ant in antonimi:
                Antonim.objects.using(database).create(
                    redni_broj=ant['redni_broj'], u_vezi_sa_id=ant['antonim_id'], tekst=ant['tekst'],
                    ima_antonim=odrednica)

        operacija_izmene_id = 2 if radimo_update else 1
        if database == 'default':
            IzmenaOdrednice.objects.using(database).create(user_id=user.id, vreme=sada, odrednica=odrednica,
                                                           operacija_izmene_id=operacija_izmene_id)
        return odrednica

    def _make_fake_pub(self, konk, database):
        try:
            retval = Publikacija.objects.using(database).get(id=konk['publikacija_id'])
            return retval
        except Publikacija.DoesNotExist:
            src_pub = Publikacija.objects.using('default').get(id=konk['publikacija_id'])
            dic = model_to_dict(src_pub)
            dic['vrsta_id'] = dic['vrsta']
            dic['user_id'] = 1
            del dic['vrsta']
            del dic['user']
            return Publikacija.objects.using(database).create(**dic)
