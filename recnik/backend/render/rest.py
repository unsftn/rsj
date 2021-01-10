from django.http import HttpResponse
from odrednice.models import Odrednica
from .renderer import render_many


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
