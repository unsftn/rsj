from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from pretraga import indexer
from .models import *
from .serializers import *


class VrstaPublikacijeList(generics.ListAPIView):
    queryset = VrstaPublikacije.objects.all()
    serializer_class = VrstaPublikacijeSerializer
    filterset_fields = ['naziv']


class VrstaPublikacijeDetail(generics.RetrieveAPIView):
    queryset = VrstaPublikacije.objects.all()
    serializer_class = VrstaPublikacijeSerializer


class PublikacijaList(generics.ListAPIView):
    queryset = Publikacija.objects.all()
    serializer_class = PublikacijaSerializer
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


JSON = 'application/json'


@api_view(['POST', 'PUT'])
def api_create_publication(request):
    if request.method == 'POST':
        serializer = CreatePublicationSerializer(data=request.data)
    else:
        try:
            pub_id = request.data['id']
            publikacija = Publikacija.objects.get(id=pub_id)
            serializer = CreatePublicationSerializer(publikacija, data=request.data)
        except (KeyError, Publikacija.DoesNotExist):
            return Response({'error': 'invalid or missing object id'}, status=status.HTTP_404_NOT_FOUND, content_type=JSON)
    if serializer.is_valid():
        publikacija = serializer.save(user=request.user)
        indexer.save_publikacija_model(publikacija)
        ser2 = PublikacijaSerializer(publikacija)
        if request.method == 'POST':
            code = status.HTTP_201_CREATED
        else:
            code = status.HTTP_204_NO_CONTENT
        return Response(ser2.data, status=code, content_type=JSON)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)


@api_view(['POST'])
def api_create_text(request):
    serializer = CreateTextSerializer(data=request.data)
    if serializer.is_valid():
        tekst_publikacije = serializer.save()
        ser2 = TekstPublikacijeSerializer(tekst_publikacije)
        retval = ser2.data
        del retval['tekst']
        return Response(retval, status=status.HTTP_201_CREATED, content_type=JSON)
    else:
        return Response({'error': 'invalid request object'}, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)
