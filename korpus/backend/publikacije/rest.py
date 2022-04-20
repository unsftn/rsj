from django.db.models import Max
from django_q.tasks import async_task
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.exceptions import NotFound, UnsupportedMediaType
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .extractor import extract_file
from .processing import extract_pdf_file, get_filter, invoke_filter, get_filter_list
from .tasks import extract_text_for_pub


class VrstaPublikacijeList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = VrstaPublikacije.objects.all()
    serializer_class = VrstaPublikacijeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['naziv']


class VrstaPublikacijeDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = VrstaPublikacije.objects.all()
    serializer_class = VrstaPublikacijeSerializer


class PotkorpusList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Potkorpus.objects.all()
    serializer_class = PotkorpusSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['naziv']


class PotkorpusDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Potkorpus.objects.all()
    serializer_class = PotkorpusSerializer


class PublikacijaList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Publikacija.objects.all()
    serializer_class = PublikacijaSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['naslov', 'naslov_izdanja', 'godina']


class PublikacijaDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Publikacija.objects.all()
    serializer_class = PublikacijaSerializer


class AutorList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['ime', 'prezime']


class AutorDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer


class TekstPublikacijeList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TekstPublikacije.objects.all()
    serializer_class = TekstPublikacijeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['publikacija_id', 'redni_broj']


class TekstPublikacijeDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TekstPublikacije.objects.all()
    serializer_class = TekstPublikacijeSerializer


class FajlPublikacijeList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = FajlPublikacije.objects.all()
    serializer_class = FajlPublikacijeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['publikacija_id', 'redni_broj']


class FajlPublikacijeDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = FajlPublikacije.objects.all()
    serializer_class = FajlPublikacijeSerializer


class FilterPublikacijeList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = FilterPublikacije.objects.all()
    serializer_class = FilterPublikacijeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['publikacija_id', 'redni_broj']


class FilterPublikacijeDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = FilterPublikacije.objects.all()
    serializer_class = FilterPublikacijeSerializer


class ParametarFilteraList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ParametarFiltera.objects.all()
    serializer_class = ParametarFilteraSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['filter_id', 'redni_broj']


class ParametarFilteraDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
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
    if serializer.is_valid():
        publikacija = serializer.save(user=request.user)
        ser2 = PublikacijaSerializer(publikacija)
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
