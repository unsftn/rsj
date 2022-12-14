from django.db.models.functions import Collate
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *


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
        queryset = RecZaOdluku.objects.filter(prvo_slovo=slovo)
        leksema = self.request.query_params.get('leksema')
        recnik = self.request.query_params.get('recnik')
        odluka = self.request.query_params.get('odluka')
        if leksema:
            queryset = queryset.filter(tekst__istartswith=leksema)
        if recnik is not None:
            recnik = recnik.capitalize() == 'False'
            queryset = queryset.filter(recnik_id__isnull=recnik)
        if odluka:
            queryset = queryset.filter(odluka=int(odluka))
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
