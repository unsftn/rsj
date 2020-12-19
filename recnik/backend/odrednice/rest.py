from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from concurrency.exceptions import RecordModifiedError
from .models import (Antonim, Sinonim, Kolokacija, RecUKolokaciji, Znacenje,
                     Podznacenje, IzrazFraza, KvalifikatorOdrednice,
                     Kvalifikator, IzmenaOdrednice, OperacijaIzmene, Odrednica)
from .serializers import (AntonimSerializer, SinonimSerializer,
                          KolokacijaSerializer, RecUKolokacijiSerializer,
                          ZnacenjeSerializer, PodznacenjeSerializer,
                          IzrazFrazaSerializer,
                          KvalifikatorOdredniceSerializer,
                          KvalifikatorSerializer, IzmenaOdredniceSerializer,
                          OperacijaIzmeneOdredniceSerializer,
                          CreateOdrednicaSerializer, OdrednicaSerializer)


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


class OdrednicaDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Odrednica.objects.all()
    serializer_class = OdrednicaSerializer


@api_view(['POST', 'PUT'])
def api_save_odrednica(request):
    if request.method == 'POST':
        serializer = CreateOdrednicaSerializer(data=request.data)
    elif request.method == 'PUT':
        try:
            odrednica_id = request.data['id']
            odrednica = Odrednica.objects.get(id=odrednica_id)
            serializer = CreateOdrednicaSerializer(odrednica,
                                                   data=request.data)
        except (KeyError, Odrednica.DoesNotExist):
            return Response({'error': 'invalid or missing object id'},
                            status=status.HTTP_404_NOT_FOUND,
                            content_type='application/json')
    if serializer.is_valid():
        try:
            odrednica = serializer.save(user_id=request.user.id)
        except RecordModifiedError:
            return Response({'error': 'optimistic lock exception'},
                            status=status.HTTP_409_CONFLICT,
                            content_type='application/json')
        ser2 = OdrednicaSerializer(odrednica)
        if request.method == 'POST':
            code = status.HTTP_201_CREATED
        else:
            code = status.HTTP_204_NO_CONTENT
        return Response(ser2.data,
                        status=code,
                        content_type='application/json')
    else:
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json')
