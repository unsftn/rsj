import logging
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

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
        fields = ('id', 'redni_broj', 'ima_antonim_id', 'u_vezi_sa_id',)


class SinonimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sinonim
        fields = ('id', 'redni_broj', 'ima_sinonim_id', 'u_vezi_sa_id',)


class KolokacijaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kolokacija
        fields = ('id', 'napomena', 'odrednica_id',)


class RecUKolokacijiSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecUKolokaciji
        fields = ('id', 'redni_broj', 'kolokacija_id', 'odrednica_id')


class KvalifikatorFrazeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KvalifikatorFraze
        fields = ('redni_broj', 'kvalifikator_id', 'izrazfraza_id',)


class IzrazFrazaSerializer(serializers.ModelSerializer):
    kvalifikatorfraze_set = KvalifikatorFrazeSerializer(many=True)

    class Meta:
        model = IzrazFraza
        fields = ('id', 'opis', 'tekst', 'redni_broj', 'odrednica_id', 'znacenje_id', 'podznacenje_id',
                  'kvalifikatorfraze_set')


class KonkordansaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Konkordansa
        fields = ('id', 'redni_broj', 'opis', 'znacenje_id', 'podznacenje_id', 'publikacija_id')


class PodznacenjeSerializer(serializers.ModelSerializer):
    kvalifikatorpodznacenja_set = KvalifikatorPodznacenjaSerializer(many=True)
    izrazfraza_set = IzrazFrazaSerializer(many=True, read_only=True)
    konkordansa_set = KonkordansaSerializer(many=True, read_only=True)

    class Meta:
        model = Podznacenje
        fields = ('id', 'tekst', 'znacenje_id', 'redni_broj', 'kvalifikatorpodznacenja_set', 'izrazfraza_set',
                  'konkordansa_set')


class ZnacenjeSerializer(serializers.ModelSerializer):
    podznacenje_set = PodznacenjeSerializer(many=True, read_only=True)
    kvalifikatorznacenja_set = KvalifikatorZnacenjaSerializer(many=True)
    izrazfraza_set = IzrazFrazaSerializer(many=True, read_only=True)
    konkordansa_set = KonkordansaSerializer(many=True, read_only=True)

    class Meta:
        model = Znacenje
        fields = ('id', 'tekst', 'znacenje_se', 'odrednica_id', 'podznacenje_set', 'kvalifikatorznacenja_set',
                  'izrazfraza_set', 'konkordansa_set', 'redni_broj')


class IzmenaOdredniceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IzmenaOdrednice
        fields = ('id', 'odrednica_id', 'operacija_izmene_id', 'user_id', 'vreme',)


class OperacijaIzmeneOdredniceSerializer(serializers.ModelSerializer):
    izmenaodrednice_set = IzmenaOdredniceSerializer(many=True, read_only=True)

    class Meta:
        model = OperacijaIzmene
        fields = ('id', 'naziv', 'izmenaodrednice_set')


class VarijantaOdredniceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VarijantaOdrednice
        fields = ('id', 'redni_broj', 'tekst', 'ijekavski', 'nastavak')


class OdrednicaSerializer(serializers.ModelSerializer):
    imaantonim_set = AntonimSerializer(many=True, read_only=True)
    antonimuvezi_set = AntonimSerializer(many=True, read_only=True)
    imasinonim_set = SinonimSerializer(many=True, read_only=True)
    sinonimuvezi_set = SinonimSerializer(many=True, read_only=True)
    kolokacija_set = KolokacijaSerializer(many=True, read_only=True)
    recukolokaciji_set = RecUKolokacijiSerializer(many=True, read_only=True)
    znacenje_set = ZnacenjeSerializer(many=True, read_only=True)
    izrazfraza_set = IzrazFrazaSerializer(many=True, read_only=True)
    varijantaodrednice_set = VarijantaOdredniceSerializer(many=True, read_only=True)
    kvalifikatorodrednice_set = KvalifikatorOdredniceSerializer(many=True, read_only=True)
    izmenaodrednice_set = IzmenaOdredniceSerializer(many=True, read_only=True)

    class Meta:
        model = Odrednica
        fields = ('id', 'rec', 'ijekavski', 'vrsta', 'rod', 'nastavak', 'info', 'glagolski_vid', 'glagolski_rod',
                  'prezent', 'broj_pregleda', 'vreme_kreiranja', 'poslednja_izmena', 'stanje', 'version',
                  'varijantaodrednice_set', 'imaantonim_set', 'imasinonim_set', 'antonimuvezi_set', 'sinonimuvezi_set',
                  'kolokacija_set', 'recukolokaciji_set', 'znacenje_set', 'izrazfraza_set',
                  'kvalifikatorodrednice_set', 'izmenaodrednice_set', 'opciono_se')


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


class CreateUpdateKolokacijaSerializer(NoSaveSerializer):
    pass


class CreateRecUKolokacijiSerializer(NoSaveSerializer):
    pass


class CreateIzrazFrazaSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    opis = serializers.CharField(max_length=2000, allow_blank=True)
    tekst = serializers.CharField(max_length=200, required=False, allow_blank=True)
    kvalifikatori = serializers.ListField(child=CreatePojavaKvalifikatoraSerializer(), required=False)


class CreateKonkordansaSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    opis = serializers.CharField(max_length=2000, allow_blank=True)
    publikacija_id = serializers.IntegerField(required=False)


class CreatePodznacenjeSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    tekst = serializers.CharField(max_length=2000, required=False, allow_blank=True)
    kvalifikatori = serializers.ListField(child=CreatePojavaKvalifikatoraSerializer(), required=False)
    izrazi_fraze = serializers.ListField(child=CreateIzrazFrazaSerializer(), required=False)
    konkordanse = serializers.ListField(child=CreateKonkordansaSerializer(), required=False)


class CreateZnacenjeSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    tekst = serializers.CharField(max_length=2000, required=False, allow_blank=True)
    znacenje_se = serializers.BooleanField()
    podznacenja = serializers.ListField(child=CreatePodznacenjeSerializer(), required=False)
    kvalifikatori = serializers.ListField(child=CreatePojavaKvalifikatoraSerializer(), required=False)
    izrazi_fraze = serializers.ListField(child=CreateIzrazFrazaSerializer(), required=False)
    konkordanse = serializers.ListField(child=CreateKonkordansaSerializer(), required=False)


class CreateSinonimSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    sinonim_id = serializers.IntegerField()


class CreateAntonimSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    antonim_id = serializers.IntegerField()


class CreateVarijantaOdredniceSerializer(NoSaveSerializer):
    redni_broj = serializers.IntegerField()
    tekst = serializers.CharField(max_length=50)
    ijekavski = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    nastavak = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)


class CreateOdrednicaSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    rec = serializers.CharField(max_length=50)
    ijekavski = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    vrsta = serializers.IntegerField(required=False)
    rod = serializers.IntegerField(required=False, allow_null=True)
    nastavak = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    info = serializers.CharField(max_length=2000, required=False, allow_blank=True, allow_null=True)
    glagolski_vid = serializers.IntegerField(required=False, allow_null=True)
    glagolski_rod = serializers.IntegerField(required=False, allow_null=True)
    prezent = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    stanje = serializers.IntegerField(required=False, allow_null=True)
    version = serializers.IntegerField(required=False, allow_null=True)
    opciono_se = serializers.NullBooleanField(required=False)
    znacenja = serializers.ListField(child=CreateZnacenjeSerializer())
    kvalifikatori = serializers.ListField(child=CreatePojavaKvalifikatoraSerializer(), required=False)
    varijante = serializers.ListField(child=CreateVarijantaOdredniceSerializer(), required=False)
    izrazi_fraze = serializers.ListField(child=CreateIzrazFrazaSerializer(), required=False)
    sinonimi = serializers.ListField(child=CreateSinonimSerializer(), required=False)
    antonimi = serializers.ListField(child=CreateAntonimSerializer(), required=False)

    def create(self, validated_data):
        return self._save(validated_data)

    def update(self, instance, validated_data):
        Znacenje.objects.filter(odrednica_id=instance.id).delete()
        IzrazFraza.objects.filter(odrednica_id=instance.id).delete()
        KvalifikatorOdrednice.objects.filter(odrednica_id=instance.id).delete()
        # TODO: delete all related objects properly
        # Antonim.objects.filter(ima_antonim_id=instance.id).delete()
        # Sinonim.objects.filter(ima_sinonim_id=instance.id).delete()
        # Kolokacija.objects.filter(odrednica_id=instance.id).delete()
        # RecUKolokaciji.objects.filter(odrednica_id=instance.id).delete()

        return self._save(validated_data, instance)

    def _save(self, validated_data, odrednica=None):
        radimo_update = odrednica is None
        user = validated_data.pop('user')
        odrednica_id = validated_data.get('id')

        sada = now()
        znacenja = validated_data.pop('znacenja', [])
        kvalifikatori_odrednice = validated_data.pop('kvalifikatori', [])
        varijante = validated_data.pop('varijante', [])
        izrazi_fraze = validated_data.pop('izrazi_fraze', [])
        sinonimi = validated_data.pop('sinonimi', [])
        antonimi = validated_data.pop('antonimi', [])

        odrednica, created = Odrednica.objects.update_or_create(defaults=validated_data, id=odrednica_id)

        for var_odr in varijante:
            VarijantaOdrednice.objects.create(odrednica=odrednica, **var_odr)
        for kvod in kvalifikatori_odrednice:
            KvalifikatorOdrednice.objects.create(odrednica=odrednica, **kvod)
        for izr_frz in izrazi_fraze:
            kvalifikatori_fraze = izr_frz.pop('kvalifikatori', [])
            iz = IzrazFraza.objects.create(odrednica=odrednica, **izr_frz)
            for kv in kvalifikatori_fraze:
                KvalifikatorFraze.objects.create(izrazfraza=iz, **kv)
        for znacenje in znacenja:
            kvalifikatori = znacenje.pop('kvalifikatori', [])
            podznacenja = znacenje.pop('podznacenja', [])
            izrazi_fraze_znacenja = znacenje.pop('izrazi_fraze', [])
            konkordanse_znacenja = znacenje.pop('konkordanse', [])
            z = Znacenje.objects.create(odrednica=odrednica, **znacenje)
            for k in kvalifikatori:
                KvalifikatorZnacenja.objects.create(znacenje=z, **k)
            for ifz in izrazi_fraze_znacenja:
                kvalifikatori_fraze = ifz.pop('kvalifikatori', [])
                IzrazFraza.objects.create(znacenje=z, **ifz)
                for kv in kvalifikatori_fraze:
                    KvalifikatorFraze.objects.create(izrazfraza=iz, **kv)
            for konz in konkordanse_znacenja:
                Konkordansa.objects.create(znacenje=z, **konz)
            for podz in podznacenja:
                kvalifikatori_podznacenja = podz.pop('kvalifikatori', [])
                izrazi_fraze_podznacenja = podz.pop('izrazi_fraze', [])
                konkordanse_podznacenja = podz.pop('konkordanse', [])
                p = Podznacenje.objects.create(znacenje=z, **podz)
                for k in kvalifikatori_podznacenja:
                    KvalifikatorPodznacenja.objects.create(podznacenje=p, **k)
                for ifp in izrazi_fraze_podznacenja:
                    kvalifikatori_fraze = ifp.pop('kvalifikatori', [])
                    IzrazFraza.objects.create(podznacenje=p, **ifp)
                    for kv in kvalifikatori_fraze:
                        KvalifikatorFraze.objects.create(izrazfraza=iz, **kv)
                for konz in konkordanse_podznacenja:
                    Konkordansa.objects.create(podznacenje=p, **konz)
        for sin in sinonimi:
            Sinonim.objects.create(redni_broj=sin['redni_broj'], u_vezi_sa_id=sin['sinonim_id'], ima_sinonim=odrednica)
        for ant in antonimi:
            Antonim.objects.create(redni_broj=ant['redni_broj'], u_vezi_sa_id=ant['antonim_id'], ima_antonim=odrednica)

        operacija_izmene_id = 2 if radimo_update else 1
        IzmenaOdrednice.objects.create(user_id=user.id, vreme=sada, odrednica=odrednica,
                                       operacija_izmene_id=operacija_izmene_id)
        return odrednica
