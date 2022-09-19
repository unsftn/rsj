# coding=utf-8
import random
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from concurrency.exceptions import RecordModifiedError
from .models import *
from .serializers import *
from indexer.index import *


class ImenicaList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Imenica.objects.all()
    serializer_class = ImenicaSerializer
    filter_fields = ['nomjed']


class ImenicaDetail(generics.RetrieveAPIView):
    queryset = Imenica.objects.all()
    serializer_class = ImenicaSerializer


class GlagolList(generics.ListAPIView):
    queryset = Glagol.objects.all()
    serializer_class = GlagolSerializer
    filter_fields = ['infinitiv']


class GlagolDetail(generics.RetrieveAPIView):
    queryset = Glagol.objects.all()
    serializer_class = GlagolSerializer


class PridevList(generics.ListAPIView):
    queryset = Pridev.objects.all()
    serializer_class = PridevSerializer
    filter_fields = ['lema']


class PridevDetail(generics.RetrieveAPIView):
    queryset = Pridev.objects.all()
    serializer_class = PridevSerializer


class PredlogList(generics.ListAPIView):
    queryset = Predlog.objects.all()
    serializer_class = PredlogSerializer
    filter_fields = ['tekst']


class PredlogDetail(generics.RetrieveAPIView):
    queryset = Predlog.objects.all()
    serializer_class = PredlogSerializer


class ReccaList(generics.ListAPIView):
    queryset = Recca.objects.all()
    serializer_class = ReccaSerializer
    filter_fields = ['tekst']


class ReccaDetail(generics.RetrieveAPIView):
    queryset = Recca.objects.all()
    serializer_class = ReccaSerializer


class UzvikList(generics.ListAPIView):
    queryset = Uzvik.objects.all()
    serializer_class = UzvikSerializer
    filter_fields = ['tekst']


class UzvikDetail(generics.RetrieveAPIView):
    queryset = Uzvik.objects.all()
    serializer_class = UzvikSerializer


class VeznikList(generics.ListAPIView):
    queryset = Veznik.objects.all()
    serializer_class = VeznikSerializer
    filter_fields = ['tekst']


class VeznikDetail(generics.RetrieveAPIView):
    queryset = Veznik.objects.all()
    serializer_class = VeznikSerializer


class ZamenicaList(generics.ListAPIView):
    queryset = Zamenica.objects.all()
    serializer_class = ZamenicaSerializer


class ZamenicaDetail(generics.RetrieveAPIView):
    queryset = Zamenica.objects.all()
    serializer_class = ZamenicaSerializer


class BrojList(generics.ListAPIView):
    queryset = Broj.objects.all()
    serializer_class = BrojSerializer


class BrojDetail(generics.RetrieveAPIView):
    queryset = Broj.objects.all()
    serializer_class = BrojSerializer


class PrilogList(generics.ListAPIView):
    queryset = Prilog.objects.all()
    serializer_class = PrilogSerializer


class PrilogDetail(generics.RetrieveAPIView):
    queryset = Prilog.objects.all()
    serializer_class = PrilogSerializer


JSON = 'application/json'


@api_view(['POST', 'PUT'])
def save_imenica(request):
    if request.method == 'POST':
        serializer = SaveImenicaSerializer(data=request.data)
    else:
        try:
            imenica_id = request.data['id']
            imenica = Imenica.objects.get(id=imenica_id)
            serializer = SaveImenicaSerializer(imenica, data=request.data)
        except (KeyError, Imenica.DoesNotExist):
            raise PermissionDenied(detail='Покушано ажурирање непостојеће именице', code=404)
    if serializer.is_valid():
        try:
            imenica = serializer.save(user=request.user)
            index_imenica(imenica)
        except RecordModifiedError:
            raise PermissionDenied(detail='Оптимистичко закључавање: неко други је у међувремену мењао именицу', code=409)
        ser2 = ImenicaSerializer(imenica)
        if request.method == 'POST':
            code = status.HTTP_201_CREATED
        else:
            code = status.HTTP_204_NO_CONTENT
        return Response(ser2.data, status=code, content_type=JSON)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)


@api_view(['POST', 'PUT'])
def save_glagol(request):
    if request.method == 'POST':
        serializer = SaveGlagolSerializer(data=request.data)
    else:
        try:
            glagol_id = request.data['id']
            glagol = Glagol.objects.get(id=glagol_id)
            serializer = SaveGlagolSerializer(glagol, data=request.data)
        except (KeyError, Glagol.DoesNotExist):
            raise PermissionDenied(detail='Покушано ажурирање непостојећег глагола', code=404)
    if serializer.is_valid():
        try:
            glagol = serializer.save(user=request.user)
            index_glagol(glagol)
        except RecordModifiedError:
            raise PermissionDenied(detail='Оптимистичко закључавање: неко други је у међувремену мењао глагол', code=409)
        ser2 = GlagolSerializer(glagol)
        if request.method == 'POST':
            code = status.HTTP_201_CREATED
        else:
            code = status.HTTP_204_NO_CONTENT
        return Response(ser2.data, status=code, content_type=JSON)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)


@api_view(['POST', 'PUT'])
def save_pridev(request):
    if request.method == 'POST':
        serializer = SavePridevSerializer(data=request.data)
    else:
        try:
            pridev_id = request.data['id']
            pridev = Pridev.objects.get(id=pridev_id)
            serializer = SavePridevSerializer(pridev, data=request.data)
        except (KeyError, Pridev.DoesNotExist):
            raise PermissionDenied(detail='Покушано ажурирање непостојећег придева', code=404)
    if serializer.is_valid():
        try:
            pridev = serializer.save(user=request.user)
            index_pridev(pridev)
        except RecordModifiedError:
            raise PermissionDenied(detail='Оптимистичко закључавање: неко други је у међувремену мењао придев', code=409)
        ser2 = PridevSerializer(pridev)
        if request.method == 'POST':
            code = status.HTTP_201_CREATED
        else:
            code = status.HTTP_204_NO_CONTENT
        return Response(ser2.data, status=code, content_type=JSON)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)


@api_view(['POST', 'PUT'])
def save_predlog(request):
    if request.method == 'POST':
        serializer = SavePredlogSerializer(data=request.data)
    else:
        try:
            predlog_id = request.data['id']
            predlog = Predlog.objects.get(id=predlog_id)
            serializer = SavePredlogSerializer(predlog, data=request.data)
        except (KeyError, Predlog.DoesNotExist):
            raise PermissionDenied(detail='Покушано ажурирање непостојећег предлога', code=404)
    if serializer.is_valid():
        try:
            predlog = serializer.save(user=request.user)
            index_predlog(predlog)
        except RecordModifiedError:
            raise PermissionDenied(detail='Оптимистичко закључавање: неко други је у међувремену мењао предлог', code=409)
        ser2 = PredlogSerializer(predlog)
        if request.method == 'POST':
            code = status.HTTP_201_CREATED
        else:
            code = status.HTTP_204_NO_CONTENT
        return Response(ser2.data, status=code, content_type=JSON)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)


@api_view(['POST', 'PUT'])
def save_recca(request):
    if request.method == 'POST':
        serializer = SaveReccaSerializer(data=request.data)
    else:
        try:
            recca_id = request.data['id']
            recca = Recca.objects.get(id=recca_id)
            serializer = SaveReccaSerializer(recca, data=request.data)
        except (KeyError, Recca.DoesNotExist):
            raise PermissionDenied(detail='Покушано ажурирање непостојеће речце', code=404)
    if serializer.is_valid():
        try:
            recca = serializer.save(user=request.user)
            index_recca(recca)
        except RecordModifiedError:
            raise PermissionDenied(detail='Оптимистичко закључавање: неко други је у међувремену мењао речцу', code=409)
        ser2 = ReccaSerializer(recca)
        if request.method == 'POST':
            code = status.HTTP_201_CREATED
        else:
            code = status.HTTP_204_NO_CONTENT
        return Response(ser2.data, status=code, content_type=JSON)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)


@api_view(['POST', 'PUT'])
def save_uzvik(request):
    if request.method == 'POST':
        serializer = SaveUzvikSerializer(data=request.data)
    else:
        try:
            uzvik_id = request.data['id']
            uzvik = Uzvik.objects.get(id=uzvik_id)
            serializer = SaveUzvikSerializer(uzvik, data=request.data)
        except (KeyError, Uzvik.DoesNotExist):
            raise PermissionDenied(detail='Покушано ажурирање непостојећег узвика', code=404)
    if serializer.is_valid():
        try:
            uzvik = serializer.save(user=request.user)
            index_uzvik(uzvik)
        except RecordModifiedError:
            raise PermissionDenied(detail='Оптимистичко закључавање: неко други је у међувремену мењао узвик', code=409)
        ser2 = UzvikSerializer(uzvik)
        if request.method == 'POST':
            code = status.HTTP_201_CREATED
        else:
            code = status.HTTP_204_NO_CONTENT
        return Response(ser2.data, status=code, content_type=JSON)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)


@api_view(['POST', 'PUT'])
def save_veznik(request):
    if request.method == 'POST':
        serializer = SaveVeznikSerializer(data=request.data)
    else:
        try:
            veznik_id = request.data['id']
            veznik = Veznik.objects.get(id=veznik_id)
            serializer = SaveVeznikSerializer(veznik, data=request.data)
        except (KeyError, Veznik.DoesNotExist):
            raise PermissionDenied(detail='Покушано ажурирање непостојећег везника', code=404)
    if serializer.is_valid():
        try:
            veznik = serializer.save(user=request.user)
            index_veznik(veznik)
        except RecordModifiedError:
            raise PermissionDenied(detail='Оптимистичко закључавање: неко други је у међувремену мењао везник', code=409)
        ser2 = VeznikSerializer(veznik)
        if request.method == 'POST':
            code = status.HTTP_201_CREATED
        else:
            code = status.HTTP_204_NO_CONTENT
        return Response(ser2.data, status=code, content_type=JSON)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)


@api_view(['POST', 'PUT'])
def save_zamenica(request):
    if request.method == 'POST':
        serializer = SaveZamenicaSerializer(data=request.data)
    else:
        try:
            zamenica_id = request.data['id']
            zamenica = Zamenica.objects.get(id=zamenica_id)
            serializer = SaveZamenicaSerializer(zamenica, data=request.data)
        except (KeyError, Zamenica.DoesNotExist):
            raise PermissionDenied(detail='Покушано ажурирање непостојеће заменице', code=404)
    if serializer.is_valid():
        try:
            zamenica = serializer.save(user=request.user)
            index_zamenica(zamenica)
        except RecordModifiedError:
            raise PermissionDenied(detail='Оптимистичко закључавање: неко други је у међувремену мењао заменицу', code=409)
        ser2 = ZamenicaSerializer(zamenica)
        if request.method == 'POST':
            code = status.HTTP_201_CREATED
        else:
            code = status.HTTP_204_NO_CONTENT
        return Response(ser2.data, status=code, content_type=JSON)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)


@api_view(['POST', 'PUT'])
def save_broj(request):
    if request.method == 'POST':
        serializer = SaveBrojSerializer(data=request.data)
    else:
        try:
            broj_id = request.data['id']
            broj = Broj.objects.get(id=broj_id)
            serializer = SaveBrojSerializer(broj, data=request.data)
        except (KeyError, Broj.DoesNotExist):
            raise PermissionDenied(detail='Покушано ажурирање непостојећег броја', code=404)
    if serializer.is_valid():
        try:
            broj = serializer.save(user=request.user)
            index_broj(broj)
        except RecordModifiedError:
            raise PermissionDenied(detail='Оптимистичко закључавање: неко други је у међувремену мењао број', code=409)
        ser2 = BrojSerializer(broj)
        if request.method == 'POST':
            code = status.HTTP_201_CREATED
        else:
            code = status.HTTP_204_NO_CONTENT
        return Response(ser2.data, status=code, content_type=JSON)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)


@api_view(['POST', 'PUT'])
def save_prilog(request):
    if request.method == 'POST':
        serializer = SavePrilogSerializer(data=request.data)
    else:
        try:
            prilog_id = request.data['id']
            prilog = Prilog.objects.get(id=prilog_id)
            serializer = SavePrilogSerializer(prilog, data=request.data)
        except (KeyError, Prilog.DoesNotExist):
            raise PermissionDenied(detail='Покушано ажурирање непостојећег прилога', code=404)
    if serializer.is_valid():
        try:
            prilog = serializer.save(user=request.user)
            index_prilog(prilog)
        except RecordModifiedError:
            raise PermissionDenied(detail='Оптимистичко закључавање: неко други је у међувремену мењао прилог', code=409)
        ser2 = PrilogSerializer(prilog)
        if request.method == 'POST':
            code = status.HTTP_201_CREATED
        else:
            code = status.HTTP_204_NO_CONTENT
        return Response(ser2.data, status=code, content_type=JSON)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)


@api_view(['PUT'])
def change_password(request):
    try:
        user = UserProxy.objects.get(id=request.user.id)
        new_password = request.data['newPassword']
        user.set_password(new_password)
        user.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    except:
        raise ValidationError(detail='Није могуће променити лозинку', code=400)


@api_view(['POST'])
@csrf_exempt
@permission_classes([permissions.AllowAny])
def forgot_password(request):
    try:
        email = request.data['email']
        user = UserProxy.objects.get(email=email)
        new_password = generate_password()
        user.set_password(new_password)
        user.save()
        send_mail('Nova lozinka za Korpus',
                  EMAIL_TEXT % new_password,
                  'recnik@uns.ac.rs',
                  [email],
                  fail_silently=True)
        return Response({}, status=status.HTTP_201_CREATED)
    except:
        raise ValidationError(detail='Непознат корисник', code=404)


@api_view(['GET'])
def get_broj_reci_za_korisnika(request):
    try:
        user = request.user
        bur = get_brojac_reci(user.id)
        return Response(bur, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(-1, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_broj_reci_za_sve(request):
    retval = []
    for bur in BrojacUnetihReci.objects.all():
        retval.append({
            'user': {
                'id': bur.user.id, 
                'first_name': bur.user.first_name,
                'last_name': bur.user.last_name,
                'email': bur.user.email,
            },
            'broj_unetih_reci': bur.broj_reci,
        })
    return Response(retval, status=status.HTTP_200_OK)


from django.db.models import Count
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_statistika_unosa_reci(request):
    result = []
    for user in UserProxy.objects.all():
        imenice = Imenica.objects.filter(vlasnik=user).count()
        glagoli = Glagol.objects.filter(vlasnik=user).count()
        pridevi = Pridev.objects.filter(vlasnik=user).count()
        prilozi = Prilog.objects.filter(vlasnik=user).count()
        zamenice = Zamenica.objects.filter(vlasnik=user).count()
        predlozi = Predlog.objects.filter(vlasnik=user).count()
        uzvici = Uzvik.objects.filter(vlasnik=user).count()
        veznici = Veznik.objects.filter(vlasnik=user).count()
        recce = Recca.objects.filter(vlasnik=user).count()
        brojevi = Broj.objects.filter(vlasnik=user).count()
        ukupno = imenice + glagoli + pridevi + prilozi + predlozi + zamenice + uzvici + veznici + recce + brojevi
        item = {
            'ime': user.first_name, 
            'prezime': user.last_name, 
            'email': user.email, 
            'imenice': imenice,
            'glagoli': glagoli,
            'pridevi': pridevi,
            'prilozi': prilozi,
            'zamenice': zamenice,
            'predlozi': predlozi,
            'uzvici': uzvici,
            'veznici': veznici,
            'recce': recce,
            'brojevi': brojevi,
            'ukupno': ukupno
        }
        result.append(item)
    return Response(result, status=status.HTTP_200_OK)


def generate_password():
    digits = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V",
              "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    random.shuffle(digits)
    return "".join(digits[:12])


EMAIL_TEXT = """

Poštovani,

Zatražili ste kreiranje nove lozinke za sajt Korpusa srpskog jezika. 

Vaša nova lozinka je %s

---
pozdrav,
RSJ
"""
