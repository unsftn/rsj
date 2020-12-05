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


@api_view(['POST'])
def api_create_publication(request):
    serializer = CreatePublicationSerializer(data=request.data)
    if serializer.is_valid():
        publikacija = serializer.save()
        ser2 = PublikacijaSerializer(publikacija)
        return Response(ser2.data, status=status.HTTP_200_OK, content_type='application/json')
    else:
        return Response({'error': 'invalid request object'}, status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json')
