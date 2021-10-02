# coding=utf-8
# from django.core.mail import send_mail
# from django.db.models.functions import Collate
# from django.http import HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from concurrency.exceptions import RecordModifiedError
from .models import *
from .serializers import *


class ImenicaList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Imenica.objects.all()
    serializer_class = ImenicaSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['nomjed']


class ImenicaDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Imenica.objects.all()
    serializer_class = ImenicaSerializer


class GlagolList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Glagol.objects.all()
    serializer_class = GlagolSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['infinitiv']


class GlagolDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Glagol.objects.all()
    serializer_class = GlagolSerializer


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
