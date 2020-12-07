from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *


class VrstaImeniceList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = VrstaImenice.objects.all()
    serializer_class = VrstaImeniceSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['naziv']


class VrstaImeniceDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = VrstaImenice.objects.all()
    serializer_class = VrstaImeniceSerializer


class ImenicaList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Imenica.objects.all()
    serializer_class = ImenicaSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['vrsta_id', 'nomjed', 'vreme']


class ImenicaDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Imenica.objects.all()
    serializer_class = ImenicaSerializer


class GlagolList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Glagol.objects.all()
    serializer_class = GlagolSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['vid', 'rod', 'vreme']


class GlagolDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Glagol.objects.all()
    serializer_class = GlagolSerializer


class PridevList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Pridev.objects.all()
    serializer_class = PridevSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['vreme']


class PridevDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Pridev.objects.all()
    serializer_class = PridevSerializer


@api_view(['POST', 'PUT'])
def api_save_imenica(request):
    pass


@api_view(['POST', 'PUT'])
def api_save_glagol(request):
    pass


@api_view(['POST', 'PUT'])
def api_save_pridev(request):
    pass
