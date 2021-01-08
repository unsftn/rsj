from rest_framework import serializers
from django.utils.timezone import now
from .models import (Antonim, Sinonim, Kolokacija, RecUKolokaciji, IzrazFraza,
                     Podznacenje, Znacenje, Kvalifikator, Odrednica,
                     KvalifikatorOdrednice, IzmenaOdrednice, OperacijaIzmene)


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


class IzrazFrazaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IzrazFraza
        fields = ('id', 'opis', 'u_vezi_sa_id', 'pripada_odrednici_id',)


class PodznacenjeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podznacenje
        fields = ('id', 'tekst', 'znacenje_id',)


class ZnacenjeSerializer(serializers.ModelSerializer):
    podznacenje_set = PodznacenjeSerializer(many=True, read_only=True)

    class Meta:
        model = Znacenje
        fields = ('id', 'tekst', 'odrednica_id', 'podznacenje_set',)


class KvalifikatorOdredniceSerializer(serializers.ModelSerializer):
    class Meta:
        model = KvalifikatorOdrednice
        fields = ('id', 'redni_broj', 'kvalifikator_id', 'odrednica_id',)


class KvalifikatorSerializer(serializers.ModelSerializer):
    kvalifikatorodrednice_set = KvalifikatorOdredniceSerializer(many=True,
                                                                read_only=True)

    class Meta:
        model = Kvalifikator
        fields = ('id', 'naziv', 'kvalifikatorodrednice_set')


class IzmenaOdredniceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IzmenaOdrednice
        fields = ('id', 'odrednica_id', 'operacija_izmene_id', 'user_id',
                  'vreme',)


class OperacijaIzmeneOdredniceSerializer(serializers.ModelSerializer):
    izmenaodrednice_set = IzmenaOdredniceSerializer(many=True, read_only=True)

    class Meta:
        model = OperacijaIzmene
        fields = ('id', 'naziv', 'izmenaodrednice_set')


class OdrednicaSerializer(serializers.ModelSerializer):
    imaantonim_set = AntonimSerializer(many=True, read_only=True)
    antonimuvezi_set = AntonimSerializer(many=True, read_only=True)
    imasinonim_set = SinonimSerializer(many=True, read_only=True)
    sinonimuvezi_set = SinonimSerializer(many=True, read_only=True)
    kolokacija_set = KolokacijaSerializer(many=True, read_only=True)
    recukolokaciji_set = RecUKolokacijiSerializer(many=True, read_only=True)
    znacenje_set = ZnacenjeSerializer(many=True, read_only=True)
    izrazfraza_set = IzrazFrazaSerializer(many=True, read_only=True)
    izrazfrazapripada_set = IzrazFrazaSerializer(many=True, read_only=True)
    kvalifikatorodrednice_set = KvalifikatorOdredniceSerializer(many=True,
                                                                read_only=True)
    izmenaodrednice_set = IzmenaOdredniceSerializer(many=True, read_only=True)

    class Meta:
        model = Odrednica
        fields = ('id', 'rec', 'vrsta', 'rod', 'nastavak', 'info',
                  'glagolski_vid', 'glagolski_rod', 'prezent',
                  'broj_pregleda', 'vreme_kreiranja', 'poslednja_izmena',
                  'stanje', 'version', 'imaantonim_set', 'imasinonim_set',
                  'antonimuvezi_set', 'sinonimuvezi_set', 'kolokacija_set',
                  'recukolokaciji_set', 'znacenje_set', 'izrazfraza_set',
                  'izrazfrazapripada_set', 'kvalifikatorodrednice_set',
                  'izmenaodrednice_set')


class CreateUpdateIzrazFrazaSerializer(serializers.Serializer):

    def create(self, validated_data):
        return IzrazFraza(**validated_data)

    def update(self, instance, validated_data):
        instance.opis = validated_data.get('opis')
        instance.save()
        return instance


class CreateKvalifikatorOdredniceSerializer(serializers.Serializer):

    def create(self, validated_data):
        return KvalifikatorOdrednice(**validated_data)

    def update(self, instance, validated_data):
        # nema azuriranja
        return instance


class CreateUpdateKvalifikatorSerializer(serializers.Serializer):

    def create(self, validated_data):
        return Kvalifikator(**validated_data)

    def update(self, instance, validated_data):
        instance.naziv = validated_data.get('naziv')
        instance.save()
        return instance


class CreateIzmenaOdredniceSerializer(serializers.Serializer):
    vreme = serializers.DateTimeField()
    user_id = serializers.IntegerField()
    operacija_izmene_id = serializers.IntegerField()

    def create(self, validated_data):
        return IzmenaOdrednice(**validated_data)

    def update(self, instance, validated_data):
        # nema azuriranja
        return instance


class CreateUpdateOperacijaIzmeneSerializer(serializers.Serializer):

    def create(self, validated_data):
        return OperacijaIzmene(**validated_data)

    def update(self, instance, validated_data):
        instance.naziv = validated_data.get('naziv')
        instance.save()
        return instance


class CreateAntonimSerializer(serializers.Serializer):

    def create(self, validated_data):
        return Antonim(**validated_data)

    def update(self, instance, validated_data):
        # nikad ne radimo update
        return instance


class CreateSinonimSerializer(serializers.Serializer):

    def create(self, validated_data):
        return Sinonim(**validated_data)

    def update(self, instance, validated_data):
        # nikad ne radimo update
        return instance


class CreateUpdateKolokacijaSerializer(serializers.Serializer):

    def create(self, validated_data):
        return Kolokacija(**validated_data)

    def update(self, instance, validated_data):
        instance.napomena = validated_data.get('napomena')
        instance.save()
        return instance


class CreateRecUKolokacijiSerializer(serializers.Serializer):

    def create(self, validated_data):
        return RecUKolokaciji(**validated_data)

    def update(self, instance, validated_data):
        # nikad ne radimo update
        return instance


class CreateUpdateZnacenjeSerializer(serializers.Serializer):

    def create(self, validated_data):
        return Znacenje(**validated_data)

    def update(self, instance, validated_data):
        instance.tekst = validated_data.get('tekst')
        instance.save()
        return instance


class CreateUpdatePodznacenjeSerializer(serializers.Serializer):

    def create(self, validated_data):
        return Podznacenje(**validated_data)

    def update(self, instance, validated_data):
        instance.tekst = validated_data.get('tekst')
        instance.save()
        return instance


class CreateOdrednicaSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    rec = serializers.CharField(max_length=50, required=False, allow_blank=True)
    vrsta = serializers.IntegerField(required=False)
    rod = serializers.IntegerField(required=False)
    nastavak = serializers.CharField(max_length=50, required=False, allow_blank=True)
    info = serializers.CharField(max_length=2000, required=False, allow_blank=True)
    glagolski_vid = serializers.IntegerField(required=False)
    glagolski_rod = serializers.IntegerField(required=False)
    prezent = serializers.CharField(max_length=50, required=False, allow_blank=True)
    broj_pregleda = serializers.IntegerField(required=False)
    stanje = serializers.IntegerField(required=False)
    version = serializers.IntegerField(required=False)

    def create(self, validated_data):
        sada = now()
        user_id = validated_data['user_id']
        del validated_data['user_id']
        odrednica = Odrednica.objects.create(vreme_kreiranja=sada, poslednja_izmena=sada, **validated_data)
        naziv = 'Kreiranje odrednice: ' + str(odrednica.id)
        operacija_izmene = OperacijaIzmene.objects.create(naziv=naziv)
        IzmenaOdrednice.objects.create(user_id=user_id, vreme=sada, odrednica=odrednica,
                                       operacija_izmene=operacija_izmene)
        return odrednica

    def update(self, instance, validated_data):
        sada = now()
        user_id = validated_data['user_id']
        del validated_data['user_id']
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        Antonim.objects.filter(ima_antonim_id=instance).delete()
        Antonim.objects.filter(u_vezi_sa_id=instance).delete()
        Sinonim.objects.filter(ima_sinonim_id=instance).delete()
        Sinonim.objects.filter(u_vezi_sa_id=instance).delete()
        Kolokacija.objects.filter(odrednica=instance).delete()
        RecUKolokaciji.objects.filter(odrednica=instance).delete()
        Znacenje.objects.filter(odrednica=instance).delete()
        IzrazFraza.objects.filter(u_vezi_sa_id=instance).delete()
        IzrazFraza.objects.filter(pripada_odrednici_id=instance).delete()
        KvalifikatorOdrednice.objects.filter(odrednica=instance).delete()

        instance.version += 1
        instance.poslednja_izmena = sada
        instance.save()
        naziv = 'Azuriranje odrednice: ' + str(instance.id)
        operacija_izmene = OperacijaIzmene.objects.create(naziv=naziv)
        IzmenaOdrednice.objects.create(user_id=user_id, vreme=sada,
                                       odrednica=instance,
                                       operacija_izmene=operacija_izmene)
        return instance
