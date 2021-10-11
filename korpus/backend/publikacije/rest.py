from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *


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
