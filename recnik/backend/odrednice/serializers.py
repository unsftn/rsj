import logging
from django.forms.models import model_to_dict
from rest_framework import serializers
from render.utils import shorten_text, get_rec, get_rbr
from .models import *
from django.contrib.auth.models import User

log = logging.getLogger(__name__)
AZBUKA = 'абвгдђежзијклљмнњопрстћуфхцчџш'


def get_sinant(clazz, src_vrsta: int, src_id: int):
    retval = []
    part1 = [{'vrsta': s.vrsta2, 'ident': s.ident2} for s in clazz.objects.filter(vrsta1=src_vrsta, ident1=src_id)]
    part2 = [{'vrsta': s.vrsta1, 'ident': s.ident1} for s in clazz.objects.filter(vrsta2=src_vrsta, ident2=src_id)]
    retval.extend(part1)
    retval.extend(part2)
    for r in retval:
        if r['vrsta'] == 1:
            try:
                o = Odrednica.objects.get(id=r['ident'])
                r['tekst'] = ''
                r['odr'] = get_rec(o)
                r['rbr'] = ''
            except Odrednica.DoesNotExist:
                log.warn(f'[get_sinant] Odrednica {r["ident"]} nije pronadjena')
        elif r['vrsta'] == 2:
            try:
                z = Znacenje.objects.get(id=r['ident'])
                o = z.odrednica
                r['tekst'] = shorten_text(z.tekst)
                r['odr'] = get_rec(z.odrednica)
                r['rbr'] = get_rbr(z)
            except Znacenje.DoesNotExist:
                log.warn(f'[get_sinant] Znacenje {r["ident"]} nije pronadjeno')
        elif r['vrsta'] == 3:
            try:
                pz = Podznacenje.objects.get(id=r['ident'])
                o = pz.znacenje.odrednica
                r['tekst'] = shorten_text(pz.tekst)
                r['odr'] = get_rec(pz.znacenje.odrednica)
                r['rbr'] = get_rbr(pz)
            except Podznacenje.DoesNotExist:
                log.warn(f'[get_sinant] Podznacenje {r["ident"]} nije pronadjeno')
            except IndexError:
                log.warn(f'[get_sinant] Podznacenje ima redni_broj = {pz.redni_broj} > 30')
    return retval


def obrisi_veze(clazz, odrednica):
    clazz.objects.filter(ident1=odrednica.id, vrsta1=1).delete()
    clazz.objects.filter(ident2=odrednica.id, vrsta2=1).delete()
    clazz.objects.filter(ident1__in=[x.id for x in odrednica.znacenje_set.all()], vrsta1=2).delete()
    clazz.objects.filter(ident2__in=[x.id for x in odrednica.znacenje_set.all()], vrsta2=2).delete()
    clazz.objects.filter(ident1__in=[x.id for x in Podznacenje.objects.filter(znacenje__in=odrednica.znacenje_set.all())], vrsta1=3).delete()
    clazz.objects.filter(ident2__in=[x.id for x in Podznacenje.objects.filter(znacenje__in=odrednica.znacenje_set.all())], vrsta2=3).delete()


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
        fields = ('id', 'redni_broj', 'vrsta1', 'ident1', 'vrsta2', 'ident2', 'tekst')


class SinonimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sinonim
        fields = ('id', 'redni_broj', 'vrsta1', 'ident1', 'vrsta2', 'ident2', 'tekst')


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


class KonkordansaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Konkordansa
        fields = ('id', 'redni_broj', 'opis', 'znacenje_id', 'podznacenje_id', 'izraz_fraza_id', 'korpus_izvor_id')


class IzrazFrazaSerializer(serializers.ModelSerializer):
    kvalifikatorfraze_set = KvalifikatorFrazeSerializer(many=True)
    konkordansa_set = KonkordansaSerializer(many=True)

    class Meta:
        model = IzrazFraza
        fields = ('id', 'opis', 'tekst', 'redni_broj', 'odrednica_id', 'znacenje_id', 'podznacenje_id',
                  'kvalifikatorfraze_set', 'vezana_odrednica_id', 'konkordansa_set')


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
    sinonimi = serializers.SerializerMethodField()
    antonimi = serializers.SerializerMethodField()

    def get_sinonimi(self, obj):
        return get_sinant(Sinonim, 3, obj.id)

    def get_antonimi(self, obj):
        return get_sinant(Antonim, 3, obj.id)

    class Meta:
        model = Podznacenje
        fields = ('id', 'tekst', 'znacenje_id', 'redni_broj', 'kvalifikatorpodznacenja_set', 'izrazfraza_set',
                  'konkordansa_set', 'kolokacijapodznacenja_set', 'sinonimi', 'antonimi')


class ZnacenjeSerializer(serializers.ModelSerializer):
    podznacenje_set = PodznacenjeSerializer(many=True, read_only=True)
    kvalifikatorznacenja_set = KvalifikatorZnacenjaSerializer(many=True)
    izrazfraza_set = IzrazFrazaSerializer(many=True, read_only=True)
    konkordansa_set = KonkordansaSerializer(many=True, read_only=True)
    kolokacijaznacenja_set = KolokacijaZnacenjaSerializer(many=True, read_only=True)
    sinonimi = serializers.SerializerMethodField()
    antonimi = serializers.SerializerMethodField()

    def get_sinonimi(self, obj):
        return get_sinant(Sinonim, 2, obj.id)

    def get_antonimi(self, obj):
        return get_sinant(Antonim, 2, obj.id)

    class Meta:
        model = Znacenje
        fields = ('id', 'tekst', 'znacenje_se', 'odrednica_id', 'podznacenje_set', 'kvalifikatorznacenja_set',
                  'izrazfraza_set', 'konkordansa_set', 'redni_broj', 'kolokacijaznacenja_set',
                  'sinonimi', 'antonimi')


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
                  'opciono_se', 'rod')  # , 'ravnopravna')


class StatusOdredniceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusOdrednice
        fields = ('id', 'naziv')


class PodvrstaReciSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodvrstaReci
        fields = ('id', 'vrsta', 'naziv', 'skracenica')


class OdrednicaSerializer(serializers.ModelSerializer):
    kolokacija_set = KolokacijaSerializer(many=True, read_only=True)
    znacenje_set = ZnacenjeSerializer(many=True, read_only=True)
    izrazfraza_set = IzrazFrazaSerializer(many=True, read_only=True)
    varijantaodrednice_set = VarijantaOdredniceSerializer(many=True, read_only=True)
    kvalifikatorodrednice_set = KvalifikatorOdredniceSerializer(many=True, read_only=True)
    izmenaodrednice_set = IzmenaOdredniceSerializer(many=True, read_only=True)
    podvrsta = PodvrstaReciSerializer(read_only=True)
    sinonimi = serializers.SerializerMethodField()
    antonimi = serializers.SerializerMethodField()

    def get_sinonimi(self, obj):
        return get_sinant(Sinonim, 1, obj.id)

    def get_antonimi(self, obj):
        return get_sinant(Antonim, 1, obj.id)

    class Meta:
        model = Odrednica
        fields = ('id', 'rec', 'ijekavski', 'vrsta', 'rod', 'nastavak', 'nastavak_ij', 'info', 'glagolski_vid',
                  'glagolski_rod', 'prezent', 'prezent_ij', 'broj_pregleda', 'vreme_kreiranja', 'poslednja_izmena',
                  'stanje', 'version', 'varijantaodrednice_set', 'podvrsta', 'sortable_rec',
                  'kolokacija_set', 'znacenje_set', 'izrazfraza_set', 'kvalifikatorodrednice_set',
                  'izmenaodrednice_set', 'opciono_se', 'rbr_homonima', 'obradjivac', 'redaktor', 'urednik', 'napomene',
                  'freetext', 'status', 'prikazi_gl_rod', 'ima_se_znacenja', 'ravnopravne_varijante',
                  'sinonimi', 'antonimi')


class ShortOdrednicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Odrednica
        fields = ('id', 'rec', 'vrsta', 'vreme_kreiranja', 'poslednja_izmena', 'stanje', 'obradjivac', 'redaktor',
                  'urednik', 'status', 'napomene')


class MediumOdrednicaSerializer(serializers.ModelSerializer):
    status = StatusOdredniceSerializer()
    obradjivac = UserSerializer()
    redaktor = UserSerializer() 
    urednik = UserSerializer()
    class Meta:
        model = Odrednica
        fields = ('id', 'rec', 'vrsta', 'vreme_kreiranja', 'poslednja_izmena', 'stanje', 'obradjivac', 'redaktor',
                  'urednik', 'status', 'napomene')

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


class CreateKonkordansaSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    opis = serializers.CharField(max_length=2000, allow_blank=True)
    # publikacija_id = serializers.IntegerField(required=False, allow_null=True)
    korpus_izvor_id = serializers.IntegerField(required=False, allow_null=True)


class CreateIzrazFrazaSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    opis = serializers.CharField(max_length=2000, allow_blank=True)
    tekst = serializers.CharField(max_length=200, required=False, allow_blank=True)
    kvalifikatori = serializers.ListField(child=CreatePojavaKvalifikatoraSerializer(), required=False)
    konkordanse = serializers.ListField(child=CreateKonkordansaSerializer(), required=False)
    vezana_odrednica_id = serializers.IntegerField(required=False, allow_null=True)


class CreateSinonimSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    vrsta2 = serializers.IntegerField()
    ident2 = serializers.IntegerField()
    tekst = serializers.CharField(allow_null=True, allow_blank=True, required=False)


class CreateAntonimSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    vrsta2 = serializers.IntegerField()
    ident2 = serializers.IntegerField()
    tekst = serializers.CharField(allow_null=True, allow_blank=True, required=False)


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
    sinonimi = serializers.ListField(child=CreateSinonimSerializer(), required=False, allow_empty=True)
    antonimi = serializers.ListField(child=CreateAntonimSerializer(), required=False, allow_empty=True)


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
    sinonimi = serializers.ListField(child=CreateSinonimSerializer(), required=False, allow_empty=True)
    antonimi = serializers.ListField(child=CreateAntonimSerializer(), required=False, allow_empty=True)


class CreateVarijantaOdredniceSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    tekst = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    ijekavski = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    nastavak = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    nastavak_ij = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    prezent = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    prezent_ij = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    opciono_se = serializers.BooleanField(required=False, allow_null=True)
    rod = serializers.IntegerField(required=False, allow_null=True)
    # ravnopravna = serializers.BooleanField()


class CreateOdrednicaSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    rec = serializers.CharField(max_length=50)
    ijekavski = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    vrsta = serializers.IntegerField(required=False)
    podvrsta_id = serializers.IntegerField(required=False, allow_null=True)
    rod = serializers.IntegerField(required=False, allow_null=True)
    nastavak = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    nastavak_ij = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    info = serializers.CharField(max_length=2000, required=False, allow_blank=True, allow_null=True)
    glagolski_vid = serializers.IntegerField(required=False, allow_null=True)
    glagolski_rod = serializers.IntegerField(required=False, allow_null=True)
    prikazi_gl_rod = serializers.BooleanField(required=False, allow_null=True)
    ima_se_znacenja = serializers.BooleanField(required=False, allow_null=True)
    prezent = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    prezent_ij = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    stanje = serializers.IntegerField(required=False, allow_null=True)
    version = serializers.IntegerField(required=False, allow_null=True)
    opciono_se = serializers.BooleanField(required=False, allow_null=True)
    napomene = serializers.CharField(max_length=2000, required=False, allow_blank=True, allow_null=True)
    freetext = serializers.CharField(max_length=2000, required=False, allow_blank=True, allow_null=True)
    znacenja = serializers.ListField(child=CreateZnacenjeSerializer())
    kvalifikatori = serializers.ListField(child=CreatePojavaKvalifikatoraSerializer(), required=False)
    varijante = serializers.ListField(child=CreateVarijantaOdredniceSerializer(), required=False)
    izrazi_fraze = serializers.ListField(child=CreateIzrazFrazaSerializer(), required=False)
    sinonimi = serializers.ListField(child=CreateSinonimSerializer(), required=False, allow_empty=True)
    antonimi = serializers.ListField(child=CreateAntonimSerializer(), required=False, allow_empty=True)
    rbr_homonima = serializers.IntegerField(required=False, allow_null=True)
    kolokacije = serializers.ListField(child=CreateKolokacijaSerializer(), required=False)
    status_id = serializers.IntegerField(required=False, allow_null=True)
    ravnopravne_varijante = serializers.BooleanField(required=False, allow_null=True)

    def instantiate(self):
        return self._save(self.validated_data, None, 'memory')

    def create(self, validated_data):
        return self._save(validated_data)

    def update(self, instance, validated_data):
        return self._save(validated_data, instance)

    def _save(self, validated_data, odrednica=None, database='default'):
        sada = now()
        radimo_update = odrednica is not None
        user = validated_data.pop('user') if database == 'default' else None

        odrednica_id = validated_data.get('id')

        znacenja = validated_data.pop('znacenja', [])
        kvalifikatori_odrednice = validated_data.pop('kvalifikatori', [])
        varijante = validated_data.pop('varijante', [])
        izrazi_fraze = validated_data.pop('izrazi_fraze', [])
        kolokacije = validated_data.pop('kolokacije', [])
        sinonimi = validated_data.pop('sinonimi', [])
        antonimi = validated_data.pop('antonimi', [])

        validated_data['poslednja_izmena'] = sada
        if database == 'default':
            if validated_data['stanje'] == 1 and not odrednica_id:
                validated_data['obradjivac'] = user
            elif validated_data['stanje'] == 2 and not odrednica_id:
                validated_data['redaktor'] = user
            elif validated_data['stanje'] == 3 and not odrednica_id:
                validated_data['urednik'] = user
        if database == 'default':
            validated_data['obradjivac'] = user
            validated_data['poslednja_izmena'] = sada
        odrednica, created = Odrednica.objects.using(database).update_or_create(id=odrednica_id, defaults=validated_data)
        if not created:
            Znacenje.objects.filter(odrednica_id=odrednica.id).delete()
            IzrazFraza.objects.filter(odrednica_id=odrednica.id).delete()
            KvalifikatorOdrednice.objects.filter(odrednica_id=odrednica.id).delete()
            VarijantaOdrednice.objects.filter(odrednica_id=odrednica.id).delete()
            Kolokacija.objects.filter(odrednica_id=odrednica.id).delete()
            obrisi_veze(Sinonim, odrednica)
            obrisi_veze(Antonim, odrednica)

        for var_odr in varijante:
            VarijantaOdrednice.objects.using(database).create(odrednica=odrednica, **var_odr)
        for kvod in kvalifikatori_odrednice:
            KvalifikatorOdrednice.objects.using(database).create(odrednica=odrednica, **kvod)
        for izr_frz in izrazi_fraze:
            kvalifikatori_fraze = izr_frz.pop('kvalifikatori', [])
            konkordanse_fraze = izr_frz.pop('konkordanse', [])
            if database != 'default' and izr_frz.get('vezana_odrednica_id'):
                izr_frz['vezana_odrednica_id'] = None
            iz = IzrazFraza.objects.using(database).create(odrednica=odrednica, **izr_frz)
            for kv in kvalifikatori_fraze:
                KvalifikatorFraze.objects.using(database).create(izrazfraza=iz, **kv)
            for kk in konkordanse_fraze:
                # if database != 'default' and kk.get('publikacija_id'):
                #     dst_pub = self._make_fake_pub(kk, database)
                #     del kk['publikacija_id']
                #     Konkordansa.objects.using(database).create(izraz_fraza=iz, publikacija=dst_pub, **kk)
                # else:
                    Konkordansa.objects.using(database).create(izraz_fraza=iz, **kk)
        for s in sinonimi:
            Sinonim.objects.create(ident1=odrednica.id, vrsta1=1, **s)
        for a in antonimi:
            Antonim.objects.create(ident1=odrednica.id, vrsta1=1, **a)
        for znacenje in znacenja:
            kvalifikatori = znacenje.pop('kvalifikatori', [])
            podznacenja = znacenje.pop('podznacenja', [])
            izrazi_fraze_znacenja = znacenje.pop('izrazi_fraze', [])
            konkordanse_znacenja = znacenje.pop('konkordanse', [])
            kolokacije_znacenja = znacenje.pop('kolokacije', [])
            sinonimi_z = znacenje.pop('sinonimi', [])
            antonimi_z = znacenje.pop('antonimi', [])
            z = Znacenje.objects.using(database).create(odrednica=odrednica, **znacenje)
            for k in kvalifikatori:
                KvalifikatorZnacenja.objects.using(database).create(znacenje=z, **k)
            for ifz in izrazi_fraze_znacenja:
                konkordanse1 = ifz.pop('konkordanse', [])
                kvalifikatori_fraze = ifz.pop('kvalifikatori', [])
                if database != 'default' and ifz.get('vezana_odrednica_id'):
                    ifz['vezana_odrednica_id'] = None
                iz = IzrazFraza.objects.using(database).create(znacenje=z, **ifz)
                for kv in kvalifikatori_fraze:
                    KvalifikatorFraze.objects.using(database).create(izrazfraza=iz, **kv)
                for kk in konkordanse1:
                    # if database != 'default' and kk.get('publikacija_id'):
                    #     dst_pub = self._make_fake_pub(kk, database)
                    #     del kk['publikacija_id']
                    #     Konkordansa.objects.using(database).create(izraz_fraza=iz, publikacija=dst_pub, **kk)
                    # else:
                        Konkordansa.objects.using(database).create(izraz_fraza=iz, **kk)
            for konz in konkordanse_znacenja:
                # if database != 'default' and konz.get('publikacija_id'):
                #     dst_pub = self._make_fake_pub(konz, database)
                #     del konz['publikacija_id']
                #     Konkordansa.objects.using(database).create(znacenje=z, publikacija=dst_pub, **konz)
                # else:
                    Konkordansa.objects.using(database).create(znacenje=z, **konz)
            for kol in kolokacije_znacenja:
                KolokacijaZnacenja.objects.using(database).create(znacenje=z, **kol)
            for s in sinonimi_z:
                Sinonim.objects.create(ident1=z.id, vrsta1=2, **s)
            for a in antonimi_z:
                Antonim.objects.create(ident1=z.id, vrsta1=2, **a)
            for podz in podznacenja:
                kvalifikatori_podznacenja = podz.pop('kvalifikatori', [])
                izrazi_fraze_podznacenja = podz.pop('izrazi_fraze', [])
                konkordanse_podznacenja = podz.pop('konkordanse', [])
                kolokacije_podznacenja = podz.pop('kolokacije', [])
                sinonimi_pz = podz.pop('sinonimi', [])
                antonimi_pz = podz.pop('antonimi', [])
                p = Podznacenje.objects.using(database).create(znacenje=z, **podz)
                for k in kvalifikatori_podznacenja:
                    KvalifikatorPodznacenja.objects.using(database).create(podznacenje=p, **k)
                for ifp in izrazi_fraze_podznacenja:
                    kvalifikatori_fraze = ifp.pop('kvalifikatori', [])
                    konkordanse2 = ifp.pop('konkordanse', [])
                    if database != 'default' and ifp.get('vezana_odrednica_id'):
                        ifp['vezana_odrednica_id'] = None
                    iz = IzrazFraza.objects.using(database).create(podznacenje=p, **ifp)
                    for kv in kvalifikatori_fraze:
                        KvalifikatorFraze.objects.using(database).create(izrazfraza=iz, **kv)
                    for kk in konkordanse2:
                        # if database != 'default' and kk.get('publikacija_id'):
                        #     dst_pub = self._make_fake_pub(kk, database)
                        #     del kk['publikacija_id']
                        #     Konkordansa.objects.using(database).create(izraz_fraza=iz, publikacija=dst_pub, **kk)
                        # else:
                            Konkordansa.objects.using(database).create(izraz_fraza=iz, **kk)
                for konz in konkordanse_podznacenja:
                    # if database != 'default' and konz.get('publikacija_id'):
                    #     dst_pub = self._make_fake_pub(konz, database)
                    #     del konz['publikacija_id']
                    #     Konkordansa.objects.using(database).create(podznacenje=p, publikacija=dst_pub, **konz)
                    # else:
                        Konkordansa.objects.using(database).create(podznacenje=p, **konz)
                for kol in kolokacije_podznacenja:
                    KolokacijaPodznacenja.objects.using(database).create(podznacenje=p, **kol)
                for s in sinonimi_pz:
                    Sinonim.objects.create(ident1=p.id, vrsta1=3, **s)
                for a in antonimi_pz:
                    Antonim.objects.create(ident1=p.id, vrsta1=3, **a)
        if database == 'default':
            for kol in kolokacije:
                odrednice = kol.pop('odrednice', [])
                k = Kolokacija.objects.using(database).create(**kol, odrednica=odrednica)
                for odr in odrednice:
                    RecUKolokaciji.objects.using(database).create(kolokacija=k, **odr)
            # for sin in sinonimi:
            #     Sinonim.objects.using(database).create(
            #         redni_broj=sin['redni_broj'], u_vezi_sa_id=sin['sinonim_id'],  tekst=sin['tekst'],
            #         ima_sinonim=odrednica)
            # for ant in antonimi:
            #     Antonim.objects.using(database).create(
            #         redni_broj=ant['redni_broj'], u_vezi_sa_id=ant['antonim_id'], tekst=ant['tekst'],
            #         ima_antonim=odrednica)

        operacija_izmene_id = 2 if radimo_update else 1
        if database == 'default':
            IzmenaOdrednice.objects.create(user_id=user.id, vreme=sada, odrednica=odrednica,
                operacija_izmene_id=operacija_izmene_id)
            # odrednica.obradjivac = user
            # odrednica.poslednja_izmena = sada
            # odrednica.save()

        return odrednica

    # def _make_fake_pub(self, konk, database):
    #     try:
    #         retval = Publikacija.objects.using(database).get(id=konk['publikacija_id'])
    #         return retval
    #     except Publikacija.DoesNotExist:
    #         src_pub = Publikacija.objects.using('default').get(id=konk['publikacija_id'])
    #         dic = model_to_dict(src_pub)
    #         dic['vrsta_id'] = dic['vrsta']
    #         dic['user_id'] = 1
    #         del dic['vrsta']
    #         del dic['user']
    #         return Publikacija.objects.using(database).create(**dic)
