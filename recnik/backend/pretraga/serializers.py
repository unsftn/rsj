import re
import unicodedata
from rest_framework import serializers
from odrednice.models import VRSTA_ODREDNICE
from odrednice.text import remove_punctuation
from .models import OdrednicaDocument, KorpusDocument, OdrednicaResponse, KorpusResponse, PublikacijaDocument
from .cyrlat import cyr_to_lat


REGEX_CONTAINS_PARENTHESES = re.compile('(.+)\\((.*?)\\)(.*?)')


def clear_accents_old(obj):
    if isinstance(obj, str):
        return ''.join(c for c in obj if unicodedata.category(c) != 'Mn')
    if isinstance(obj, list):
        new_list = []
        for item in obj:
            if isinstance(item, str):
                new_list.append(''.join(c for c in item if unicodedata.category(c) != 'Mn'))
            else:
                new_list.append(item)
        return new_list
    return obj


def clear_parentheses_old(obj):
    if not obj:
        return obj
    if isinstance(obj, str):
        if not REGEX_CONTAINS_PARENTHESES.match(obj):
            return obj
        else:
            return [REGEX_CONTAINS_PARENTHESES.sub('\\1', obj), REGEX_CONTAINS_PARENTHESES.sub('\\1\\2', obj)]
    if isinstance(obj, list):
        new_list = []
        for item in obj:
            if isinstance(item, str):
                if not REGEX_CONTAINS_PARENTHESES.match(item):
                    new_list.append(item)
                else:
                    new_list.append(REGEX_CONTAINS_PARENTHESES.sub('\\1', item))
                    new_list.append(REGEX_CONTAINS_PARENTHESES.sub('\\1\\2', item))
            else:
                new_list.append(item)
        return new_list
    return obj


def clear_text(obj):
    if not obj:
        return obj
    if isinstance(obj, str):
        if not REGEX_CONTAINS_PARENTHESES.match(obj):
            return remove_punctuation(obj)
        else:
            return [remove_punctuation(REGEX_CONTAINS_PARENTHESES.sub('\\1\\3', obj)), remove_punctuation(REGEX_CONTAINS_PARENTHESES.sub('\\1\\2\\3', obj))]
    if isinstance(obj, list):
        new_list = []
        for item in obj:
            if isinstance(item, str):
                if not REGEX_CONTAINS_PARENTHESES.match(item):
                    new_list.append(remove_punctuation(item))
                else:
                    new_list.append(remove_punctuation(REGEX_CONTAINS_PARENTHESES.sub('\\1\\3', item)))
                    new_list.append(remove_punctuation(REGEX_CONTAINS_PARENTHESES.sub('\\1\\2\\3', item)))
            else:
                new_list.append(item)
        return new_list
    return obj


def clear_accents_in_dict(obj, skip=[]):
    new_dict = {}
    for key in obj.keys():
        if key not in skip:
            new_dict[key] = clear_accents_old(obj[key])
        else:
            new_dict[key] = obj[key]
    return new_dict


def add_latin(lst):
    result = []
    result.extend(lst)
    for item in lst:
        result.append(cyr_to_lat(item))
    return result


def append_latin(tekst):
    return tekst + ' ' + cyr_to_lat(tekst)


class CreateOdrednicaDocumentSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=True)
    rec = serializers.CharField(max_length=50, required=True, allow_blank=True)
    varijante = serializers.ListField(child=serializers.CharField(), required=True)
    vrsta = serializers.IntegerField(required=True)
    rbr_homo = serializers.IntegerField(required=True, allow_null=True)

    class Meta:
        model = OdrednicaDocument
        fields = ('pk', 'rec', 'varijante', 'vrsta')

    def create(self, validated_data):
        pk = validated_data.pop('pk')
        rec = validated_data.pop('rec')
        varijante = validated_data.pop('varijante', [])
        varijante.append(rec)
        # varijante = clear_accents_old(varijante)
        # varijante = clear_parentheses_old(varijante)
        varijante = clear_text(varijante)
        varijante = add_latin(varijante)
        var_set = set(varijante)
        varijante = list(var_set)
        rec_sa_varijantama = ' '.join(varijante)
        vrsta = validated_data.pop('vrsta')
        rbr_homo = validated_data.pop('rbr_homo')

        return OdrednicaDocument(
            pk=pk,
            rec=rec,
            varijante=rec_sa_varijantama,
            vrsta=vrsta,
            rbr_homo=rbr_homo
        )


class OdrednicaResponseSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=True)
    rec = serializers.CharField(max_length=50, required=True, allow_blank=True)
    vrsta = serializers.IntegerField(required=True)
    vrsta_text = serializers.SerializerMethodField()
    rbr_homo = serializers.IntegerField(required=True, allow_null=True)

    def get_vrsta_text(self, obj):
        return VRSTA_ODREDNICE[obj.vrsta][1]

    class Meta:
        model = OdrednicaResponse
        fields = ('pk', 'rec', 'vrsta', 'vrsta_text', 'rbr_homo')


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


class CreatePublikacijaDocumentSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=True)
    skracenica = serializers.CharField(max_length=100, required=True, allow_blank=True)
    naslov = serializers.CharField(max_length=300, required=True, allow_blank=True)
    tekst = serializers.CharField(max_length=1000, required=True, allow_blank=True)

    class Meta:
        model = PublikacijaDocument
        fields = ('pk', 'skracenica', 'naslov', 'tekst')

    def create(self, validated_data):
        tekst = validated_data.pop('tekst')
        tekst = clear_accents_old(tekst)
        tekst = append_latin(tekst)
        return PublikacijaDocument(tekst=tekst, **validated_data)


class PublikacijaResponseSerializer(serializers.Serializer):
    pk = serializers.IntegerField(required=True)
    skracenica = serializers.CharField(max_length=100, required=True, allow_blank=True)
    naslov = serializers.CharField(max_length=300, required=True, allow_blank=True)

    def create(self, validated_data):
        return {
            'pk': validated_data.get('pk'),
            'skracenica': validated_data.get('skracenica'),
            'naslov': validated_data.get('naslov')
        }
