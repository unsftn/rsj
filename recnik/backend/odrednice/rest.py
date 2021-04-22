# coding=utf-8
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from concurrency.exceptions import RecordModifiedError
from pretraga import indexer
from .models import *
from .serializers import *


class AntonimList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Antonim.objects.all()
    serializer_class = AntonimSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['redni_broj']


class AntonimDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Antonim.objects.all()
    serializer_class = AntonimSerializer


class SinonimList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Sinonim.objects.all()
    serializer_class = SinonimSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['redni_broj']


class SinonimDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Sinonim.objects.all()
    serializer_class = SinonimSerializer


class KolokacijaList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Kolokacija.objects.all()
    serializer_class = KolokacijaSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['napomena']


class KolokacijaDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Kolokacija.objects.all()
    serializer_class = KolokacijaSerializer


class RecUKolokacijiList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = RecUKolokaciji.objects.all()
    serializer_class = RecUKolokacijiSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['redni_broj']


class RecUKolokacijiDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = RecUKolokaciji.objects.all()
    serializer_class = RecUKolokacijiSerializer


class ZnacenjeList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Znacenje.objects.all()
    serializer_class = ZnacenjeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['tekst']


class ZnacenjeDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Znacenje.objects.all()
    serializer_class = ZnacenjeSerializer


class PodznacenjeList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Podznacenje.objects.all()
    serializer_class = PodznacenjeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['tekst']


class PodznacenjeDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Podznacenje.objects.all()
    serializer_class = PodznacenjeSerializer


class IzrazFrazaList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = IzrazFraza.objects.all()
    serializer_class = IzrazFrazaSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['opis']


class IzrazFrazaDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = IzrazFraza.objects.all()
    serializer_class = IzrazFrazaSerializer


class KvalifikatorList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Kvalifikator.objects.all()
    serializer_class = KvalifikatorSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['naziv']


class KvalifikatorDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Kvalifikator.objects.all()
    serializer_class = KvalifikatorSerializer


class KvalifikatorOdredniceList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = KvalifikatorOdrednice.objects.all()
    serializer_class = KvalifikatorOdredniceSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['redni_broj']


class KvalifikatorOdredniceDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = KvalifikatorOdrednice.objects.all()
    serializer_class = KvalifikatorOdredniceSerializer


class KvalifikatorZnacenjaList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = KvalifikatorZnacenja.objects.all()
    serializer_class = KvalifikatorZnacenjaSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['redni_broj']


class KvalifikatorZnacenjaDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = KvalifikatorZnacenja.objects.all()
    serializer_class = KvalifikatorZnacenjaSerializer


class KvalifikatorPodznacenjaList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = KvalifikatorPodznacenja.objects.all()
    serializer_class = KvalifikatorPodznacenjaSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['redni_broj']


class KvalifikatorPodznacenjaDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = KvalifikatorPodznacenja.objects.all()
    serializer_class = KvalifikatorPodznacenjaSerializer


class IzmenaOdredniceList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = IzmenaOdrednice.objects.all()
    serializer_class = IzmenaOdredniceSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['vreme']


class IzmenaOdredniceDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = IzmenaOdrednice.objects.all()
    serializer_class = IzmenaOdredniceSerializer


class OperacijaIzmeneOdredniceList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = OperacijaIzmene.objects.all()
    serializer_class = OperacijaIzmeneOdredniceSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['naziv']


class OperacijaIzmeneOdredniceDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = OperacijaIzmene.objects.all()
    serializer_class = OperacijaIzmeneOdredniceSerializer


class OdrednicaList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Odrednica.objects.all()
    serializer_class = OdrednicaSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['rec', 'rod', 'vreme_kreiranja']


class OdrednicaLatestList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Odrednica.objects.all().order_by('-vreme_kreiranja')
    serializer_class = OdrednicaSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['rec', 'rod', 'vreme_kreiranja']


class OdrednicaChangedList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Odrednica.objects.all().order_by('-poslednja_izmena')
    serializer_class = OdrednicaSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['rec', 'rod', 'vreme_kreiranja']


class OdrednicaPopularList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Odrednica.objects.all().order_by('-broj_pregleda')
    serializer_class = OdrednicaSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['rec', 'rod', 'vreme_kreiranja']


class OdrednicaDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Odrednica.objects.all()
    serializer_class = OdrednicaSerializer


JSON = 'application/json'


@api_view(['POST', 'PUT'])
def api_save_odrednica(request):
    user = UserProxy.objects.get(id=request.user.id)
    if request.method == 'POST':
        serializer = CreateOdrednicaSerializer(data=request.data)
    elif request.method == 'PUT':
        try:
            odrednica_id = request.data['id']
            odrednica = Odrednica.objects.get(id=odrednica_id)
            if user.je_obradjivac():
                if odrednica.stanje > 1:
                    raise PermissionDenied(detail='Одредница није у фази обраде', code=403)
                if odrednica.obradjivac != user:
                    raise PermissionDenied(detail='Други обрађивач је задужен за ову одредницу', code=403)
            elif user.je_redaktor():
                if odrednica.stanje > 2:
                    raise PermissionDenied(detail='Одредница није у фази редактуре или обраде', code=403)
                if odrednica.stanje == 2 and odrednica.redaktor != user:
                    raise PermissionDenied(detail='Други редактор је задужен за ову одредницу', code=403)
            elif user.je_urednik():
                if odrednica.stanje > 3:
                    raise PermissionDenied(detail='Одредница је у стању завршене обраде', code=403)
                if odrednica.stanje == 3 and odrednica.urednik != user:
                    raise PermissionDenied(detail='Други уредник је задужен за ову одредницу', code=403)
            serializer = CreateOdrednicaSerializer(odrednica, data=request.data)
        except (KeyError, Odrednica.DoesNotExist):
            return Response({'error': 'invalid or missing object id'}, status=status.HTTP_404_NOT_FOUND, content_type=JSON)
    if serializer.is_valid():
        try:
            odrednica = serializer.save(user=request.user)
            indexer.save_odrednica_model(odrednica)
        except RecordModifiedError:
            return Response({'error': 'optimistic lock exception'}, status=status.HTTP_409_CONFLICT, content_type=JSON)
        ser2 = OdrednicaSerializer(odrednica)
        if request.method == 'POST':
            code = status.HTTP_201_CREATED
        else:
            code = status.HTTP_204_NO_CONTENT
        return Response(ser2.data, status=code, content_type=JSON)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)


@api_view(['DELETE'])
def api_delete_odrednica(request, odrednica_id):
    try:
        odrednica = Odrednica.objects.get(id=odrednica_id)
        # TODO: proveri da li korisnik ima pravo da obrise odrednicu
        odrednica.delete()
    except Odrednica.DoesNotExist:
        return Response({'error': 'entry not found'}, status=status.HTTP_404_NOT_FOUND, content_type=JSON)
    return Response({}, status=status.HTTP_204_NO_CONTENT, content_type=JSON)


@api_view(['POST'])
def api_predaj_obradjivacu(request, odrednica_id):
    user = UserProxy.objects.get(id=request.user.id)
    try:
        odrednica = Odrednica.objects.get(id=odrednica_id)
        if user.je_obradjivac():
            raise PermissionDenied(detail='Obraђивач не може вратити одредницу у обраду', code=403)
        sada = now()
        odrednica.stanje = 1
        odrednica.poslednja_izmena = sada
        odrednica.save()
        IzmenaOdrednice.objects.create(user_id=user.id, vreme=sada, odrednica=odrednica, operacija_izmene_id=3)
    except Odrednica.DoesNotExist:
        raise NotFound(detail='Одредница није пронађена', code=404)
    return Response({}, status=status.HTTP_204_NO_CONTENT, content_type=JSON)


@api_view(['POST'])
def api_predaj_redaktoru(request, odrednica_id):
    user = UserProxy.objects.get(id=request.user.id)
    try:
        odrednica = Odrednica.objects.get(id=odrednica_id)
        if user.je_obradjivac():
            if odrednica.stanje > 1:
                raise PermissionDenied(detail='Одредница није у обради', code=403)
        sada = now()
        odrednica.stanje = 2
        odrednica.poslednja_izmena = sada
        odrednica.save()
        IzmenaOdrednice.objects.create(user_id=user.id, vreme=sada, odrednica=odrednica, operacija_izmene_id=4)
    except Odrednica.DoesNotExist:
        raise NotFound(detail='Одредница није пронађена', code=404)
    return Response({}, status=status.HTTP_204_NO_CONTENT, content_type=JSON)


@api_view(['POST'])
def api_predaj_uredniku(request, odrednica_id):
    user = UserProxy.objects.get(id=request.user.id)
    try:
        odrednica = Odrednica.objects.get(id=odrednica_id)
        if odrednica.stanje != 2:
            raise PermissionDenied(detail='Одредница није у стању редактуре', code=403)
        if user.je_obradjivac():
            raise PermissionDenied(detail='Обрађивач нема права проследити одредницу уреднику', code=403)
        sada = now()
        odrednica.stanje = 3
        odrednica.poslednja_izmena = sada
        odrednica.save()
        IzmenaOdrednice.objects.create(user_id=user.id, vreme=sada, odrednica=odrednica, operacija_izmene_id=5)
    except Odrednica.DoesNotExist:
        raise NotFound(detail='Одредница није пронађена', code=404)
    return Response({}, status=status.HTTP_204_NO_CONTENT, content_type=JSON)


@api_view(['POST'])
def api_zavrsi_obradu(request, odrednica_id):
    user = UserProxy.objects.get(id=request.user.id)
    try:
        odrednica = Odrednica.objects.get(id=odrednica_id)
        if odrednica.stanje != 3:
            raise PermissionDenied(detail='Одредница није код уредника', code=403)
        if not user.je_urednik() and not user.je_administrator():
            raise PermissionDenied(detail='Само уредник има права да заврши обраду одреднице', code=403)
        sada = now()
        odrednica.stanje = 4
        odrednica.poslednja_izmena = sada
        odrednica.save()
        IzmenaOdrednice.objects.create(user_id=user.id, vreme=sada, odrednica=odrednica, operacija_izmene_id=6)
    except Odrednica.DoesNotExist:
        raise NotFound(detail='Одредница није пронађена', code=404)
    return Response({}, status=status.HTTP_204_NO_CONTENT, content_type=JSON)


@api_view(['GET'])
def api_moje_odrednice(request, page_size):
    user = UserProxy.objects.get(id=request.user.id)
    if user.je_obradjivac():
        odrednice1 = Odrednica.objects.filter(obradjivac=user, stanje=1).order_by('-poslednja_izmena')[:page_size]
        odrednice2 = Odrednica.objects.none()
    elif user.je_redaktor():
        odrednice1 = Odrednica.objects.filter(redaktor=user, stanje=2).order_by('-poslednja_izmena')[:page_size]
        odrednice2 = Odrednica.objects.filter(redaktor__isnull=True, stanje=2).order_by('-poslednja_izmena')[:page_size]
    elif user.je_urednik():
        odrednice1 = Odrednica.objects.filter(urednik=user, stanje=3).order_by('-poslednja_izmena')[:page_size]
        odrednice2 = Odrednica.objects.filter(urednik__isnull=True, stanje=3).order_by('-poslednja_izmena')[:page_size]
    else:
        odrednice1 = Odrednica.objects.order_by('-poslednja_izmena')[:page_size*2]
        odrednice2 = Odrednica.objects.none()
    result = []
    for odr in odrednice1.union(odrednice2):
        izmena = odr.izmenaodrednice_set.all().order_by('-vreme').first()
        name = izmena.user.first_name if izmena else ''
        result.append({'odrednica_id': odr.id, 'rec': odr.rec, 'datum': odr.poslednja_izmena, 'autor': name})
    return Response(result, status=status.HTTP_200_OK, content_type=JSON)
