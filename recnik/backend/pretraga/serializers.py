from rest_framework import serializers

from pretraga.models import OdrednicaDocument, KorpusDocument, OdrednicaResponse, KorpusResponse


class CreateOdrednicaDocumentSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=True)
    rec = serializers.CharField(max_length=50, required=True, allow_blank=True)
    varijante = serializers.ListField(child=serializers.CharField(), required=True)
    vrsta = serializers.IntegerField(required=True)

    class Meta:
        model = OdrednicaDocument
        fields = ('pk', 'rec', 'varijante', 'vrsta')

    def create(self, validated_data):
        pk = validated_data.pop('pk')
        rec = validated_data.pop('rec')
        varijante = validated_data.pop('varijante', [])
        recSaVarijantama = ' '.join(varijante)
        recSaVarijantama += ' ' + rec
        vrsta = validated_data.pop('vrsta')

        return OdrednicaDocument(
            pk=pk,
            rec=rec,
            varijante=recSaVarijantama,
            vrsta=vrsta
        )


class OdrednicaResponseSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=True)
    rec = serializers.CharField(max_length=50, required=True, allow_blank=True)
    vrsta = serializers.IntegerField(required=True)

    class Meta:
        model = OdrednicaResponse
        fields = ('pk', 'rec', 'vrsta')


class CreateKorpusDocumentSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=True)
    osnovniOblik = serializers.CharField(max_length=50, required=True, allow_blank=True)
    oblici = serializers.ListField(child=serializers.CharField(), required=True)

    class Meta:
        model = KorpusDocument
        fields = ('pk', 'osnovniOblik', 'oblici')

    def create(self, validated_data):
        pk = validated_data.pop('pk')
        osnovniOblik = validated_data.pop('osnovniOblik')
        oblici = validated_data.pop('oblici', [])
        sviOblici = ' '.join(oblici)
        sviOblici += ' ' + osnovniOblik

        return KorpusDocument(
            pk=pk,
            osnovniOblik=osnovniOblik,
            oblici=sviOblici
        )


class KorpusResponseSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=True)
    osnovniOblik = serializers.CharField(max_length=50, required=True, allow_blank=True)

    class Meta:
        model = KorpusResponse
        fields = ('pk', 'osnovniOblik')
