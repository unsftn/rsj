import logging
from django.http import HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from odrednice.models import Odrednica
from odrednice.serializers import CreateOdrednicaSerializer
from .renderer import render_many, render_one_div
from .models import TipRenderovanogDokumenta, RenderovaniDokument
from .serializers import *

logger = logging.getLogger(__name__)
JSON = 'application/json'


def odrednice_latest(request, page_size):
    return HttpResponse(render_odrednice_by('-poslednja_izmena', page_size).encode('UTF-8'),
                        content_type='text/html; charset=utf-8')


def odrednice_newest(request, page_size):
    return HttpResponse(render_odrednice_by('-vreme_kreiranja', page_size).encode('UTF-8'),
                        content_type='text/html; charset=utf-8')


def odrednice_popular(request, page_size):
    return HttpResponse(render_odrednice_by('-broj_pregleda', page_size).encode('UTF-8'),
                        content_type='text/html; charset=utf-8')


def render_odrednice_by(sort_order, page_size):
    """
    Vraca renderovane odrednice sortirane po kriterijumu sort_order i u kolicini page_size
    """
    odrednice = Odrednica.objects.all().order_by(sort_order)[:page_size]
    return render_many(odrednice)


@api_view(['POST'])
def api_preview_odrednica(request):
    try:
        serializer = CreateOdrednicaSerializer(data=request.data)
        if serializer.is_valid():
            odrednica = serializer.instantiate()
            text = render_one_div(odrednica)
            odrednica.delete()
            return Response(text, status=status.HTTP_200_OK, content_type='text/html')
        else:
            return Response({'serializer_errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)
    except Exception as ex:
        logger.fatal(ex)
        return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)


class TipRenderovanogDokumentaList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TipRenderovanogDokumenta.objects.all()
    serializer_class = TipRenderovanogDokumentaSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['naziv']


class TipRenderovanogDokumentaDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TipRenderovanogDokumenta.objects.all()
    serializer_class = TipRenderovanogDokumentaSerializer


class RenderovaniDokumentList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = RenderovaniDokument.objects.all().order_by('-vreme_rendera')
    serializer_class = RenderovaniDokumentSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['opis', 'vreme_rendera']


class RenderovaniDokumentDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = RenderovaniDokument.objects.all()
    serializer_class = RenderovaniDokumentSerializer
