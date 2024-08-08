import logging
from django.conf import settings
from django.utils.timezone import now
from django.db.models import F
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.response import Response
from .models import *

JSON = 'application/json'
log = logging.getLogger(__name__)


@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny])
def api_korpus(request, odrednica_id):
    user = auth_from_korpus(request)
    if request.method == 'GET':
        return _get_for_korpus(odrednica_id)
    else:
        return _save_from_korpus(odrednica_id, user, request.data)


def _get_for_korpus(odrednica_id):
    try:
        odrednica = Odrednica.objects.get(id=odrednica_id)
        retval = {
            'id': odrednica.id,
            'rec': odrednica.rec,
            'rbr_homonima': odrednica.rbr_homonima,
            'znacenja': [
                {
                    'id': z.id,
                    'rbr': z.redni_broj,
                    'tekst': z.tekst,
                    'primeri': [
                        {
                            'id': p.id,
                            'rbr': p.redni_broj,
                            'tekst': p.opis,
                            'izvor_id': p.korpus_izvor_id,
                        }
                        for p in z.konkordansa_set.all().order_by('redni_broj')
                    ],
                    'podznacenja': [
                        {
                            'id': pz.id,
                            'rbr': pz.redni_broj,
                            'tekst': pz.tekst,
                            'primeri': [
                                {
                                    'id': pr.id,
                                    'rbr': pr.redni_broj,
                                    'tekst': pr.opis,
                                    'izvor_id': pr.korpus_izvor_id,
                                }
                                for pr in pz.konkordansa_set.all().order_by('redni_broj')
                            ]
                        } for pz in z.podznacenje_set.all().order_by('redni_broj')
                    ]
                } 
                for z in odrednica.znacenje_set.all().order_by('redni_broj')
            ]
        }
        return Response(retval, status=status.HTTP_200_OK, content_type=JSON)
    except Odrednica.DoesNotExist:
        raise NotFound(detail='Одредница није пронађена', code=404)
    except Exception as ex:
        log.error(ex)
        raise NotFound(detail='Одредница није пронађена', code=500)


def _update_znacenje(zid, znacenje):
    try:
        z = Znacenje.objects.get(id=zid)
        z.tekst = znacenje.get('tekst')
        z.redni_broj = znacenje.get('rbr')
        z.save()
        return z
    except Znacenje.DoesNotExist:
        raise NotFound(detail=f'Значење није пронађено: {zid}', code=404)


def _update_podznacenje(pzid, podznacenje):
    try:
        pz = Podznacenje.objects.get(id=pzid)
        pz.tekst = podznacenje.get('tekst')
        pz.redni_broj = podznacenje.get('rbr')
        pz.save()
        return pz
    except Podznacenje.DoesNotExist:
        raise NotFound(detail=f'Подзначење није пронађено: {pzid}', code=404)
    

def _update_primer(pid, primer):
    try:
        p = Konkordansa.objects.get(id=pid)
        p.opis = primer.get('tekst')
        p.korpus_izvor_id = primer.get('izvor_id')
        p.redni_broj = primer.get('rbr')
        p.save()
    except Konkordansa.DoesNotExist:
        raise NotFound(detail=f'Пример није пронађен: {pid}', code=404)


def _insert_znacenje(odrednica, znacenje):
    z = Znacenje.objects.create(odrednica=odrednica, tekst=znacenje.get('tekst'), redni_broj=znacenje.get('rbr'))
    return z


def _insert_primer(primer, znacenje=None, podznacenje=None):
    if znacenje:
        p = Konkordansa.objects.create(znacenje=znacenje, opis=primer.get('tekst'), korpus_izvor_id=primer.get('izvor_id'), redni_broj=primer.get('rbr'))
    elif podznacenje:
        p = Konkordansa.objects.create(podznacenje=podznacenje, opis=primer.get('tekst'), korpus_izvor_id=primer.get('izvor_id'), redni_broj=primer.get('rbr'))
    else:
        raise ValidationError(detail='Пример мора бити повезан са значењем или подзначењем', code=400)
    return p


def _insert_podznacenje(znacenje, podznacenje):
    pz = Podznacenje.objects.create(znacenje=znacenje, tekst=podznacenje.get('tekst'), redni_broj=podznacenje.get('rbr'))
    return pz


def _delete_znacenja(odrednica, znacenja):
    postojeca_znacenja = list(Znacenje.objects.filter(odrednica=odrednica).values_list('id', flat=True))
    nova_znacenja = [z.get('id') for z in znacenja if z.get('id')]
    for zid in postojeca_znacenja:
        if zid not in nova_znacenja:
            Znacenje.objects.get(id=zid).delete()


def _delete_podznacenja(odrednica, znacenja):
    postojeca_podznacenja = list(Podznacenje.objects.filter(znacenje__odrednica=odrednica).values_list('id', flat=True))
    nova_podznacenja = [pz.get('id') for z in znacenja for pz in z.get('podznacenja') if pz.get('id')]
    for pzid in postojeca_podznacenja:
        if pzid not in nova_podznacenja:
            Podznacenje.objects.get(id=pzid).delete()


def _delete_primeri(odrednica, znacenja):
    postojeci_primeri = list(Konkordansa.objects.filter(znacenje__odrednica=odrednica).values_list('id', flat=True))
    primeri2 = list(Konkordansa.objects.filter(podznacenje__znacenje__odrednica=odrednica).values_list('id', flat=True))
    postojeci_primeri.extend(primeri2)
    novi_primeri = [pz.get('id') for z in znacenja for pz in z.get('primeri') if pz.get('id')]
    novi_primeri2 = [ppz.get('id') for z in znacenja for pz in z.get('podznacenja') for ppz in pz.get('primeri') if ppz.get('id')]
    novi_primeri.extend(novi_primeri2)
    for ppzid in postojeci_primeri:
        if ppzid not in novi_primeri:
            Konkordansa.objects.get(id=ppzid).delete()


def _save_from_korpus(odrednica_id, user, data):
    try:
        odrednica = Odrednica.objects.get(id=odrednica_id)
        nova_znacenja = data.get('znacenja')
        _delete_znacenja(odrednica, nova_znacenja)
        _delete_podznacenja(odrednica, nova_znacenja)
        _delete_primeri(odrednica, nova_znacenja)
        for z in data.get('znacenja'):
            zid = z.get('id')
            if zid:
                znacenje = _update_znacenje(zid, z)
            else:
                znacenje = _insert_znacenje(odrednica, z)
            for pr in z.get('primeri'):
                pid = pr.get('id')
                if pid:
                    _update_primer(pid, pr)
                else:
                    _insert_primer(pr, znacenje=znacenje)
            for pz in z.get('podznacenja'):
                pzid = pz.get('id')
                if pzid:
                    podznacenje = _update_podznacenje(pzid, pz)
                else:
                    podznacenje = _insert_podznacenje(znacenje, pz)
                for pr in pz.get('primeri'):
                    pid = pr.get('id')
                    if pid:
                        _update_primer(pid, pr)
                    else:
                        _insert_primer(pr, podznacenje=podznacenje)
        odrednica.poslednja_izmena = now()
        odrednica.obradjivac = user
        odrednica.save()
        IzmenaOdrednice.objects.create(odrednica=odrednica, user=user, operacija_izmene_id=2)
        return Response(status=status.HTTP_204_NO_CONTENT, content_type=JSON)
    except Odrednica.DoesNotExist:
        raise NotFound(detail=f'Одредница није пронађена: {odrednica_id}', code=404)    
    except Exception as ex:
        log.error(ex)
        raise Exception(detail='Грешка: {ex}', code=500)


def auth_from_korpus(request):
    """
    Check if the request is coming from the korpus app. App is authenticated by 
    the API token; the same user must exist in the recnik app.
    """
    if not request.META.get('HTTP_API_TOKEN'):
        raise PermissionDenied(detail='Недостаје API токен', code=403)
    if request.META.get('HTTP_API_TOKEN') != settings.KORPUS_API_TOKEN:
        raise PermissionDenied(detail='Неисправан API токен', code=403)
    if not request.META.get('HTTP_KORPUS_USER'):
        raise PermissionDenied(detail='Недостаје корисничко име', code=403)
    try:
        user = UserProxy.objects.get(username=request.META.get('HTTP_KORPUS_USER'))
    except UserProxy.DoesNotExist:
        raise PermissionDenied(detail='Корисник није пронађен', code=403)
    return user
