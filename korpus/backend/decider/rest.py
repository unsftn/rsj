from django.db.models.functions import Collate
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *


AZBUKA = [
    'а', 'б', 'в', 'г', 'д', 'ђ', 'е', 'ж', 'з', 'и', 'ј', 'к', 'л', 'љ', 'м',
    'н', 'њ', 'о', 'п', 'р', 'с', 'т', 'ћ', 'у', 'ф', 'х', 'ц', 'ч', 'џ', 'ш',
];


class GenerisaniSpisakList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = GenerisaniSpisak.objects.all()
    serializer_class = GenerisaniSpisakSerializer


class GenerisaniSpisakDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = GenerisaniSpisak.objects.all()
    serializer_class = GenerisaniSpisakSerializer


class RecZaOdlukuList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = RecZaOdluku.objects.all()
    serializer_class = RecZaOdlukuSerializer


class RecZaOdlukuListFilteredPaged(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RecZaOdlukuSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        slovo = self.kwargs['slovo']
        if slovo == '_':
            queryset = RecZaOdluku.objects.exclude(prvo_slovo__in=AZBUKA)
        else:
            queryset = RecZaOdluku.objects.filter(prvo_slovo=slovo)
        leksema = self.request.query_params.get('leksema')
        recnik = self.request.query_params.get('recnik')
        odluka = self.request.query_params.get('odluka')
        beleska = self.request.query_params.get('beleska')
        frekod = self.request.query_params.get('frekod')
        frekdo = self.request.query_params.get('frekdo')
        if leksema:
            queryset = queryset.filter(tekst__istartswith=leksema)
        if recnik is not None:
            recnik = recnik.capitalize() == 'False'
            queryset = queryset.filter(recnik_id__isnull=recnik)
        if odluka:
            values = [int(x) for x in odluka.split(',')]
            queryset = queryset.filter(odluka__in=values)
        if beleska is not None:
            beleska = beleska.capitalize() == 'True'
            if beleska:
                queryset = queryset.exclude(beleska='')
            else: 
                queryset = queryset.filter(beleska='')
        if frekod:
            queryset = queryset.filter(broj_pojavljivanja__gte=int(frekod))
        if frekdo:
            queryset = queryset.filter(broj_pojavljivanja__lte=int(frekdo))
        return queryset.order_by(Collate('tekst', 'utf8mb4_croatian_ci'))


class RecZaOdlukuDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = RecZaOdluku.objects.all()
    serializer_class = RecZaOdlukuSerializer


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def poslednji_spisak(request):
    try:
        ps = GenerisaniSpisak.objects.latest('id')
        ser = GenerisaniSpisakSerializer(ps)
        return Response(ser.data, status=status.HTTP_200_OK)
    except GenerisaniSpisak.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
