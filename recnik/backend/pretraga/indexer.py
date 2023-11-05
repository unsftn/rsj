import logging
import requests
from django.conf import settings
from odrednice.text import remove_punctuation
from .config import ODREDNICA_MAPPING, ODREDNICA_INDEX, get_es_client
from .utils import clear_text, add_latin

log = logging.getLogger(__name__)


def check_elasticsearch():
    try:
        r = requests.get(f'{settings.ELASTICSEARCH_HOST}/')
        if r.status_code != 200:
            return False
        json = r.json()
        if not json['version']['number']:
            return False
        if int(json['version']['number'].split('.')[0]) < 7:
            return False
        return True
    except requests.exceptions.ConnectionError:
        return False


def create_index_if_needed():
    try:
        get_es_client().indices.create(index=ODREDNICA_INDEX, mappings=ODREDNICA_MAPPING)
    except Exception as ex:
        log.fatal(ex)


def recreate_index():
    try:
        client = get_es_client()
        if client.indices.exists(index=ODREDNICA_INDEX):
            client.indices.delete(index=ODREDNICA_INDEX)
        client.indices.create(index=ODREDNICA_INDEX, mappings=ODREDNICA_MAPPING)
    except Exception as ex:
        log.fatal(ex)


def create_varijante(var_list):
    varijante = clear_text(var_list)
    varijante = add_latin(varijante)
    var_set = set(varijante)
    varijante = list(var_set)
    return ' '.join(varijante)


def save_odrednica(odrednica, client=None):
    try:
        varijante = [odrednica.rec]
        if odrednica.ijekavski:
            varijante.append(odrednica.ijekavski)
        for var in odrednica.varijantaodrednice_set.all():
            if var.tekst:
                varijante.append(var.tekst)
            if var.ijekavski:
                varijante.append(var.ijekavski)
        odr_dict = {
            'vrsta': odrednica.vrsta,
            'pk': odrednica.pk,
            'rec': odrednica.rec,
            'ociscena_rec': remove_punctuation(odrednica.rec),
            'varijante': create_varijante(varijante),
            'status': odrednica.status.id if odrednica.status else 0,
            'rbr_homo': odrednica.rbr_homonima if odrednica.rbr_homonima else None
        }
        if not client:
            client = get_es_client()
        client.index(index=ODREDNICA_INDEX, id=odrednica.pk, document=odr_dict)
        return odr_dict
    except Exception as ex:
        log.fatal(ex)
        return None

def delete_odrednica(odrednica_id):
    try:
        get_es_client().delete(index=ODREDNICA_INDEX, id=odrednica_id)
        return True
    except Exception as ex:
        log.fatal(ex)
        return False
