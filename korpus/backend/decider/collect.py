import logging
from django.utils.timezone import now
from decider.models import *
from indexer.cyrlat import lat_to_cyr
from indexer.search import get_es_client
from indexer.utils import remove_punctuation
from publikacije.models import *
from reci.models import *

log = logging.getLogger(__name__)

esclient = get_es_client()


def collect_all():
    all_words = collect_words()
    find_roots(all_words)
    update_db(all_words)


def collect_words():
    start_time = now()
    all_words = {}
    log.info('Started word collection...')
    for p in Publikacija.objects.all():
        for tekst in p.tekstpublikacije_set.all():
            content = remove_punctuation(lat_to_cyr(tekst.tekst.lower()))
            for w in content.split():
                if w: 
                    store_word(all_words, w, p.id)
    end_time = now()
    log.info(f'Word collection took {end_time-start_time}')
    return all_words


def find_roots(words):
    start_time = now()
    total_words = len(words)
    log.info(f'Finding roots of {total_words} words...')
    for index, (key, word) in enumerate(list(words.items())):
        oo = find_root(key)
        if len(oo) == 1:
            oo = oo[0]
            found_key = oo['rec']
        else:
            found_key = key
        if found_key != key:
            try:
                orig_word = words[oo['rec']]
                orig_word['count'] += word['count']
                orig_word['pubs'].update(word['pubs'])
                del words[key]
            except KeyError:
                words[oo['rec']] = word
            words[oo['rec']]['vrsta'] = oo['vrsta']
            words[oo['rec']]['id'] = oo['id']
        if index % 10000 == 0 and index > 0:
            log.info(f'Finished finding root for {index} words...')
    end_time = now()
    log.info(f'Finding roots for {total_words} words took {end_time-start_time}')


def update_db(words):
    start_time = now()
    log.info('Started database updates...')
    gs = GenerisaniSpisak.objects.create(start_time=now())
    for w in words.values():
        rec = w['tekst'] or 'x'
        rzos = RecZaOdluku.objects.filter(tekst=rec)
        if len(rzos) > 0:
            rzo = rzos[0]
            rzo.broj_publikacija = len(w['pubs'])
            rzo.broj_pojavljivanja = w['count']
            rzo.poslednje_generisanje = gs
            rzo.save()
        else:
            rzo = RecZaOdluku.objects.create(
                prvo_slovo=rec[0], 
                tekst=rec[:100], 
                odluka=1, 
                broj_publikacija=len(w['pubs']), 
                broj_pojavljivanja=w['count'],
                vreme_odluke=now(),
                poslednje_generisanje=gs)
    gs.end_time = now()
    gs.save()
    end_time = now()
    log.info(f'Database updates took {end_time-start_time}')


def store_word(all_words: dict, word: str, pub_id: int):
    try:
        w = all_words[word]
        w['count'] += 1
        old_len = len(w['pubs'])
        w['pubs'][pub_id] = pub_id
        new_len = len(w['pubs'])
    except KeyError:
        w = {
            'tekst': word,
            'pubs': {pub_id: pub_id},
            'count': 1
        }
        all_words[word] = w


def find_root(rec) -> list[dict]:
    """
    Vraca listu recnika koji identifikuju osnovni oblik za datu leksemu. Pozeljno lista
    ima jedan element (tada je nedvosmisleno kojoj reci pripada data leksema).
    """
    retval = []
    resp = esclient.search(index='reci', query={'terms': {'oblici': [rec]}})
    for hit in resp['hits']['hits']:
        osnovni_oblik = hit['_source']['rec']
        pk = hit['_source']['pk']
        vrsta, id = hit['_source']['pk'].split('_')
        vrsta, id = int(vrsta), int(id)
        retval.append({'rec': osnovni_oblik, 'pk': pk, 'vrsta': vrsta, 'id': id})
    return retval
