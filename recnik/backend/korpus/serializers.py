from rest_framework import serializers
from .models import *


class VrstaImeniceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VrstaImenice
        fields = ('id', 'naziv',)


class VarijantaImeniceSerializer(serializers.ModelSerializer):
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
    varijantaimenice_set = VarijantaImeniceSerializer(many=True, read_only=True)
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


class CreateVarijantaImeniceSerializer(serializers.Serializer):
    nomjed = serializers.CharField(max_length=50, required=False, allow_blank=True)
    genjed = serializers.CharField(max_length=50, required=False, allow_blank=True)
    datjed = serializers.CharField(max_length=50, required=False, allow_blank=True)
    akujed = serializers.CharField(max_length=50, required=False, allow_blank=True)
    vokjed = serializers.CharField(max_length=50, required=False, allow_blank=True)
    insjed = serializers.CharField(max_length=50, required=False, allow_blank=True)
    lokjed = serializers.CharField(max_length=50, required=False, allow_blank=True)
    nommno = serializers.CharField(max_length=50, required=False, allow_blank=True)
    genmno = serializers.CharField(max_length=50, required=False, allow_blank=True)
    datmno = serializers.CharField(max_length=50, required=False, allow_blank=True)
    akumno = serializers.CharField(max_length=50, required=False, allow_blank=True)
    vokmno = serializers.CharField(max_length=50, required=False, allow_blank=True)
    insmno = serializers.CharField(max_length=50, required=False, allow_blank=True)
    lokmno = serializers.CharField(max_length=50, required=False, allow_blank=True)

    def create(self, validated_data):
        return VarijantaImenice(**validated_data)

    def update(self, instance, validated_data):
        # nikad ne radimo update
        return instance


class CreateIzmenaImeniceSerializer(serializers.Serializer):
    vreme = serializers.DateTimeField()
    user_id = serializers.IntegerField()

    def create(self, validated_data):
        return IzmenaImenice(**validated_data)

    def update(self, instance, validated_data):
        # nikad ne radimo update
        return instance


class CreateImenicaSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    vrsta_id = serializers.IntegerField()
    nomjed = serializers.CharField(max_length=50, required=False, allow_blank=True)
    genjed = serializers.CharField(max_length=50, required=False, allow_blank=True)
    datjed = serializers.CharField(max_length=50, required=False, allow_blank=True)
    akujed = serializers.CharField(max_length=50, required=False, allow_blank=True)
    vokjed = serializers.CharField(max_length=50, required=False, allow_blank=True)
    insjed = serializers.CharField(max_length=50, required=False, allow_blank=True)
    lokjed = serializers.CharField(max_length=50, required=False, allow_blank=True)
    nommno = serializers.CharField(max_length=50, required=False, allow_blank=True)
    genmno = serializers.CharField(max_length=50, required=False, allow_blank=True)
    datmno = serializers.CharField(max_length=50, required=False, allow_blank=True)
    akumno = serializers.CharField(max_length=50, required=False, allow_blank=True)
    vokmno = serializers.CharField(max_length=50, required=False, allow_blank=True)
    insmno = serializers.CharField(max_length=50, required=False, allow_blank=True)
    lokmno = serializers.CharField(max_length=50, required=False, allow_blank=True)
    version = serializers.IntegerField(required=False)
    varijante = CreateVarijantaImeniceSerializer(many=True, required=False)

    def create(self, validated_data):
        sada = now()
        user_id = validated_data['user_id']
        del validated_data['user_id']
        varijante = validated_data.get('varijante')
        if varijante:
            del validated_data['varijante']
        imenica = Imenica.objects.create(vreme=sada, **validated_data)
        if varijante:
            for index, var in enumerate(varijante):
                VarijantaImenice.objects.create(imenica=imenica, redni_broj=index+1, **var)
        IzmenaImenice.objects.create(user_id=user_id, vreme=sada, imenica=imenica)
        return imenica

    def update(self, instance, validated_data):
        sada = now()
        user_id = validated_data['user_id']
        del validated_data['user_id']
        varijante = validated_data.get('varijante')
        if varijante:
            del validated_data['varijante']
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        VarijantaImenice.objects.filter(imenica=instance).delete()
        instance.version += 1
        instance.save()
        if varijante:
            for index, var in enumerate(varijante):
                VarijantaImenice.objects.create(imenica=instance, redni_broj=index+1, **var)
        IzmenaImenice.objects.create(user_id=user_id, vreme=sada, imenica=instance)
        return instance


class CreateOblikGlagolaSerializer(serializers.Serializer):
    vreme = serializers.IntegerField()
    jd1 = serializers.CharField(max_length=50, required=False, allow_blank=True)
    jd2 = serializers.CharField(max_length=50, required=False, allow_blank=True)
    jd3 = serializers.CharField(max_length=50, required=False, allow_blank=True)
    mn1 = serializers.CharField(max_length=50, required=False, allow_blank=True)
    mn2 = serializers.CharField(max_length=50, required=False, allow_blank=True)
    mn3 = serializers.CharField(max_length=50, required=False, allow_blank=True)

    def create(self, validated_data):
        return OblikGlagola(**validated_data)

    def update(self, instance, validated_data):
        # nikad ne radimo update
        return instance


class CreateIzmenaGlagolaSerializer(serializers.Serializer):
    vreme = serializers.DateTimeField()
    user_id = serializers.IntegerField()

    def create(self, validated_data):
        return IzmenaGlagola(**validated_data)

    def update(self, instance, validated_data):
        # nikad ne radimo update
        return instance


class CreateGlagolSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    infinitiv = serializers.CharField(max_length=50, required=False, allow_blank=True)
    vid = serializers.IntegerField()
    rod = serializers.IntegerField()
    rgp_mj = serializers.CharField(max_length=50, required=False, allow_blank=True)
    rgp_zj = serializers.CharField(max_length=50, required=False, allow_blank=True)
    rgp_sj = serializers.CharField(max_length=50, required=False, allow_blank=True)
    rgp_mm = serializers.CharField(max_length=50, required=False, allow_blank=True)
    rgp_zm = serializers.CharField(max_length=50, required=False, allow_blank=True)
    rgp_sm = serializers.CharField(max_length=50, required=False, allow_blank=True)
    gpp = serializers.CharField(max_length=50, required=False, allow_blank=True)
    gps = serializers.CharField(max_length=50, required=False, allow_blank=True)
    version = serializers.IntegerField(required=False)
    oblici = CreateOblikGlagolaSerializer(many=True, required=False)

    def create(self, validated_data):
        sada = now()
        user_id = validated_data['user_id']
        del validated_data['user_id']
        oblici = validated_data.get('oblici')
        if oblici:
            del validated_data['oblici']
        glagol = Glagol.objects.create(vreme=sada, **validated_data)
        if oblici:
            for index, var in enumerate(oblici):
                OblikGlagola.objects.create(glagol=glagol, **var)
        IzmenaGlagola.objects.create(user_id=user_id, vreme=sada, glagol=glagol)
        return glagol

    def update(self, instance, validated_data):
        sada = now()
        user_id = validated_data['user_id']
        del validated_data['user_id']
        oblici = validated_data.get('oblici')
        if oblici:
            del validated_data['oblici']
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        OblikGlagola.objects.filter(glagol=instance).delete()
        instance.version += 1
        instance.save()
        if oblici:
            for index, var in enumerate(oblici):
                OblikGlagola.objects.create(glagol=instance, **var)
        IzmenaGlagola.objects.create(user_id=user_id, vreme=sada, glagol=instance)
        return instance


class CreatePridevSerializer(serializers.Serializer):
    # TODO
    pass
