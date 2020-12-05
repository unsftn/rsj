from rest_framework import generics, permissions
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



