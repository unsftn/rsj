import json
from django.db.models.functions import Collate
from django.db.models import Count
from django_q.tasks import async_task
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from indexer.cyrlat import lat_to_cyr
from .models import *
from .serializers import *
from .reports import *


AZBUKA = [
    'а', 'б', 'в', 'г', 'д', 'ђ', 'е', 'ж', 'з', 'и', 'ј', 'к', 'л', 'љ', 'м',
    'н', 'њ', 'о', 'п', 'р', 'с', 'т', 'ћ', 'у', 'ф', 'х', 'ц', 'ч', 'џ', 'ш',
]


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
        potkorpus = self.request.query_params.get('potkorpus')
        beleska = self.request.query_params.get('beleska')
        frekod = self.request.query_params.get('frekod')
        frekdo = self.request.query_params.get('frekdo')
        if leksema:
            tekst = lat_to_cyr(leksema)
            queryset = queryset.filter(tekst__istartswith=tekst)
        if recnik is not None:
            recnik = recnik.capitalize() == 'False'
            queryset = queryset.filter(recnik_id__isnull=recnik)
        if odluka:
            values = [int(x) for x in odluka.split(',')]
            queryset = queryset.filter(odluka__in=values)
        # TODO: implement potkorpus filter
        # if potkorpus:
        #     values = [int(x) for x in potkorpus.split(',')]
        #     queryset = queryset.filter(potkorpus_id__in=values)
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


@api_view(['POST'])
def api_zahtev_za_izvestaj(request):
    upit = request.data
    dinizv = DinamickiIzvestaj.objects.create(upit=json.dumps(upit))
    async_task(dinamicki_izvestaj_task, dinizv.id, task_name=f'izvestaj_{dinizv.id}')
    return Response(dinizv.id, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def api_izvestaj(request, id):
    try:
        dinizv = DinamickiIzvestaj.objects.get(id=id)
        serializer = DinamickiIzvestajSerializer(dinizv)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except DinamickiIzvestaj.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def api_broj_odluka(request):
    result = {}
    for slovo in AZBUKA:
        result[slovo] = {}
        for o in ODLUKE:
            result[slovo][o[0]] = 0
    upit = RecZaOdluku.objects.all().values('prvo_slovo', 'odluka').annotate(total=Count('odluka'))
    for u in upit:
        if u['prvo_slovo'] in AZBUKA:
            result[u['prvo_slovo']][u['odluka']] = u['total']
    retval = []
    suma = {'bez': 0, 'ide': 0, 'neide': 0, 'prosireni': 0, 'brisi': 0, 'total': 0}
    for slovo in AZBUKA:
        r = result[slovo]
        retval.append({'slovo': slovo.upper(), 'bez': r[1], 'ide': r[2], 'neide': r[3], 'prosireni': r[4], 'brisi': r[5], 'total': r[1]+r[2]+r[3]+r[4]+r[5]})
        suma['bez'] += r[1]
        suma['ide'] += r[2]
        suma['neide'] += r[3]
        suma['prosireni'] += r[4]
        suma['brisi'] += r[5]
        suma['total'] += r[1]+r[2]+r[3]+r[4]+r[5]
    retval.append({'slovo': 'укупно'} | suma)
    return Response(retval, status=status.HTTP_200_OK)
