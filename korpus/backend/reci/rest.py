# coding=utf-8
# from django.core.mail import send_mail
# from django.db.models.functions import Collate
# from django.http import HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
# from concurrency.exceptions import RecordModifiedError
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
