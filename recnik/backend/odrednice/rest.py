from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from concurrency.exceptions import RecordModifiedError
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
# @permission_classes([permissions.AllowAny])
def api_save_odrednica(request):
    if request.method == 'POST':
        serializer = CreateOdrednicaSerializer(data=request.data)
    elif request.method == 'PUT':
        try:
            odrednica_id = request.data['id']
            odrednica = Odrednica.objects.get(id=odrednica_id)
            serializer = CreateOdrednicaSerializer(odrednica, data=request.data)
        except (KeyError, Odrednica.DoesNotExist):
            return Response({'error': 'invalid or missing object id'}, status=status.HTTP_404_NOT_FOUND, content_type=JSON)
    if serializer.is_valid():
        try:
            odrednica = serializer.save(user_id=request.user.id)
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
        # TODO: proveri da li korisnik ima prava da obrise odrednicu
        odrednica.delete()
    except Odrednica.DoesNotExist:
        return Response({'error': 'entry not found'}, status=status.HTTP_404_NOT_FOUND, content_type=JSON)
    return Response({}, status=status.HTTP_204_NO_CONTENT, content_type=JSON)
