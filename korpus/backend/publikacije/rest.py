from django.db.models import Max
from django_q.tasks import async_task
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.exceptions import NotFound, UnsupportedMediaType
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .extractor import extract_file
from .processing import get_filter, invoke_filter, get_filter_list
from .tasks import extract_text_for_pub
from indexer.index import index_naslov


class VrstaPublikacijeList(generics.ListAPIView):
    queryset = VrstaPublikacije.objects.all()
    serializer_class = VrstaPublikacijeSerializer
    filterset_fields = ['naziv']


class VrstaPublikacijeDetail(generics.RetrieveAPIView):
    queryset = VrstaPublikacije.objects.all()
    serializer_class = VrstaPublikacijeSerializer


class PotkorpusList(generics.ListAPIView):
    queryset = Potkorpus.objects.all()
    serializer_class = PotkorpusSerializer
    filterset_fields = ['naziv']


class PotkorpusDetail(generics.RetrieveAPIView):
    queryset = Potkorpus.objects.all()
    serializer_class = PotkorpusSerializer


class PublikacijaList(generics.ListAPIView):
    queryset = Publikacija.objects.all()
    serializer_class = PublikacijaSerializer2
    pagination_class = LimitOffsetPagination
    filterset_fields = ['naslov', 'naslov_izdanja', 'godina']


class PublikacijaDetail(generics.RetrieveAPIView):
    queryset = Publikacija.objects.all()
    serializer_class = PublikacijaSerializer


class AutorList(generics.ListAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    filterset_fields = ['ime', 'prezime']


class AutorDetail(generics.RetrieveAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer


class TekstPublikacijeList(generics.ListAPIView):
    queryset = TekstPublikacije.objects.all()
    serializer_class = TekstPublikacijeSerializer
    filterset_fields = ['publikacija_id', 'redni_broj']


class TekstPublikacijeDetail(generics.RetrieveAPIView):
    queryset = TekstPublikacije.objects.all()
    serializer_class = TekstPublikacijeSerializer


class FajlPublikacijeList(generics.ListAPIView):
    queryset = FajlPublikacije.objects.all()
    serializer_class = FajlPublikacijeSerializer
    filterset_fields = ['publikacija_id', 'redni_broj']


class FajlPublikacijeDetail(generics.RetrieveAPIView):
    queryset = FajlPublikacije.objects.all()
    serializer_class = FajlPublikacijeSerializer


class FilterPublikacijeList(generics.ListAPIView):
    queryset = FilterPublikacije.objects.all()
    serializer_class = FilterPublikacijeSerializer
    filterset_fields = ['publikacija_id', 'redni_broj']


class FilterPublikacijeDetail(generics.RetrieveAPIView):
    queryset = FilterPublikacije.objects.all()
    serializer_class = FilterPublikacijeSerializer


class ParametarFilteraList(generics.ListAPIView):
    queryset = ParametarFiltera.objects.all()
    serializer_class = ParametarFilteraSerializer
    filterset_fields = ['filter_id', 'redni_broj']


class ParametarFilteraDetail(generics.RetrieveAPIView):
    queryset = ParametarFiltera.objects.all()
    serializer_class = ParametarFilteraSerializer


JSON = 'application/json'


@api_view(['POST', 'PUT'])
def api_create_publication(request):
    if request.method == 'POST':
        serializer = SavePublikacijaSerializer(data=request.data)
    else:
        try:
            pub_id = request.data['id']
            publikacija = Publikacija.objects.get(id=pub_id)
            serializer = SavePublikacijaSerializer(publikacija, data=request.data)
        except (KeyError, Publikacija.DoesNotExist):
            return Response({'error': 'invalid or missing object id'}, status=status.HTTP_404_NOT_FOUND, content_type=JSON)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)
    if serializer.is_valid():
        publikacija = serializer.save(user=request.user)
        ser2 = PublikacijaSerializer(publikacija)
        index_naslov(publikacija.id)
        code = status.HTTP_201_CREATED if request.method == 'POST' else status.HTTP_204_NO_CONTENT
        return Response(ser2.data, status=code, content_type=JSON)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)


@api_view(['POST', 'PUT'])
def api_create_text(request):
    if request.method == 'POST':
        serializer = SaveTekstPublikacijeSerializer(data=request.data)
    else:
        try:
            tpid = request.data['id']
            tekst_publikacije = TekstPublikacije.objects.get(id=tpid)
            serializer = SaveTekstPublikacijeSerializer(tekst_publikacije, data=request.data)
        except (KeyError, TekstPublikacije.DoesNotExist):
            return Response({'error': 'invalid or missing object id'}, status=status.HTTP_404_NOT_FOUND, content_type=JSON)
    if serializer.is_valid():
        tekst_publikacije = serializer.save(user=request.user)
        ser2 = TekstPublikacijeSerializer(tekst_publikacije)
        code = status.HTTP_201_CREATED if request.method == 'POST' else status.HTTP_204_NO_CONTENT
        return Response(ser2.data, status=code, content_type=JSON)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)


@api_view(['GET', 'PUT'])
def api_tekst(request, pid, fid):
    if request.method == 'GET':
        try:
            tp = TekstPublikacije.objects.get(publikacija_id=pid, redni_broj=fid)
            serializer = TekstPublikacijeSerializer(tp)
            return Response(serializer.data, status=status.HTTP_200_OK, content_type=JSON)
        except TekstPublikacije.DoesNotExist:
            return Response({'error': 'text not found'}, status=status.HTTP_404_NOT_FOUND, content_type=JSON)
    else:
        try:
            tagovan_tekst = request.body.decode('utf-8')
            tp = TekstPublikacije.objects.get(publikacija_id=pid, redni_broj=fid)
            tp.tagovan_tekst = tagovan_tekst
            tp.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT, content_type=JSON)
        except TekstPublikacije.DoesNotExist:
            return Response({'error': 'text not found'}, status=status.HTTP_404_NOT_FOUND, content_type=JSON)
        except UnicodeDecodeError:
            return Response({'error': 'unicode decoding failed'}, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def api_add_files_to_pub(request, pub_id):
    try:
        publikacija = Publikacija.objects.get(id=pub_id)
        file_count = FajlPublikacije.objects.filter(publikacija=publikacija).count()
        redni_broj = file_count + 1
        for item in request.FILES:
            file = request.FILES[item]
            FajlPublikacije.objects.create(
                publikacija=publikacija,
                redni_broj=redni_broj,
                uploaded_file=file)
            redni_broj += 1
        return Response({}, status=status.HTTP_201_CREATED, content_type=JSON)
    except Publikacija.DoesNotExist:
        raise NotFound()


@api_view(['POST'])
def api_remove_files_from_pub(request, pub_id):
    try:
        publikacija = Publikacija.objects.get(id=pub_id)
        file_ids = request.data
        if file_ids:
            FajlPublikacije.objects.filter(id__in=file_ids).delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT, content_type=JSON)
    except Publikacija.DoesNotExist:
        raise NotFound()
    except FajlPublikacije.DoesNotExist:
        raise NotFound()


@api_view(['POST'])
def api_reorder_files(request, pub_id):
    try:
        publikacija = Publikacija.objects.get(id=pub_id)
        ordered_ids = request.data
        for index, oid in enumerate(ordered_ids):
            fp = FajlPublikacije.objects.get(id=oid)
            fp.redni_broj = index + 1
            fp.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT, content_type=JSON)
    except Publikacija.DoesNotExist:
        raise NotFound()
    except FajlPublikacije.DoesNotExist:
        raise NotFound()


@api_view(['DELETE'])
def api_delete_texts_for_pub(request, pub_id):
    try:
        Publikacija.objects.get(id=pub_id)
        TekstPublikacije.objects.filter(publikacija_id=pub_id).delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT, content_type=JSON)
    except Publikacija.DoesNotExist:
        raise NotFound()


@api_view(['PUT'])
def api_extract_text_for_pub(request, pub_id):
    try:
        Publikacija.objects.get(id=pub_id)
        async_task(extract_text_for_pub, pub_id)
        return Response({}, status=status.HTTP_204_NO_CONTENT, content_type=JSON)
    except Publikacija.DoesNotExist:
        raise NotFound()


@api_view(['PUT'])
def api_set_filters(request, pub_id):
    """
    PUT /api/rezultati/save/filters/<pub_id>/
    [{
      "vrsta": 1,
      "params": [{
        "naziv": "tekst",
        "vrednost": "tekst koji se uklanja"
      }]
    }]
    """
    try:
        publikacija = Publikacija.objects.get(id=pub_id)
        FilterPublikacije.objects.filter(publikacija=publikacija).delete()
        filters = request.data
        for i, fil in enumerate(filters):
            f = FilterPublikacije.objects.create(publikacija=publikacija, redni_broj=i+1, vrsta_filtera=fil['vrsta'])
            for j, p in enumerate(fil['params']):
                ParametarFiltera.objects.create(filter=f, redni_broj=j+1, naziv=p['naziv'], vrednost=p['vrednost'])
        return Response({}, status=status.HTTP_204_NO_CONTENT, content_type=JSON)
    except Publikacija.DoesNotExist:
        raise NotFound()


@api_view(['PUT'])
def api_apply_filters(request, pub_id):
    try:
        publikacija = Publikacija.objects.get(id=pub_id)
        filteri = []
        for f in FilterPublikacije.objects.filter(publikacija=publikacija).order_by('redni_broj'):
            params = []
            for p in ParametarFiltera.objects.filter(filter=f).order_by('redni_broj'):
                params.append({'name': p.naziv, 'value': p.vrednost})
            fil = get_filter(f.vrsta_filtera)
            if fil:
                filteri.append({'filter': fil, 'params': params})
        tekstovi = TekstPublikacije.objects.filter(publikacija=publikacija).order_by('redni_broj')
        for tekst in tekstovi:
            page_text = tekst.tekst
            for fil in filteri:
                page_text = invoke_filter(fil['filter']['code'], fil['params'], page_text, tekst.redni_broj)
            tekst.tekst = page_text
            tekst.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT, content_type=JSON)
    except Publikacija.DoesNotExist:
        raise NotFound()


@api_view(['GET'])
def api_filter_list(request):
    return Response(get_filter_list(), status=status.HTTP_200_OK, content_type=JSON)
