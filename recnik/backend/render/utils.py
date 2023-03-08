import logging
from odrednice.models import Odrednica, Znacenje, Podznacenje

log = logging.getLogger(__name__)
AZBUKA = 'абвгдђежзијклљмнњопрстћуфхцчџш'


def shorten_text(text, max_length=60):
    return (text[:max_length-3] + '...') if len(text) > max_length else text


def get_rec(odrednica, html=True):
    homo = f'<sup>{str(odrednica.rbr_homonima)}</sup>' if html else str(odrednica.rbr_homonima)
    return odrednica.rec + (f' {homo}' if odrednica.rbr_homonima else '')


def get_rbr(obj):
    if isinstance(obj, Odrednica):
        return ''
    elif isinstance(obj, Znacenje):
        return str(obj.redni_broj)
    elif isinstance(obj, Podznacenje):
        if obj.redni_broj > len(AZBUKA):
            log.warn(f'Redni broj podznacenja [{obj.id}] je veci od 30: {{obj.redni_broj}}')
            return str(obj.redni_broj)
        return str(obj.znacenje.redni_broj) + AZBUKA[obj.redni_broj-1]
    else:
        log.fatal(f'Funkcija pozvana za parametar neocekivanog tipa {type(obj)}: {obj}')
        return ''
