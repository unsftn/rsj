import logging
from django.utils.timezone import now
from decider.models import *
from indexer.cyrlat import lat_to_cyr
from indexer.search import get_es_client, get_rsj_client
from indexer.utils import remove_punctuation
from publikacije.models import *
from reci.models import *

log = logging.getLogger(__name__)

esclient = get_es_client()
rsjclient = get_rsj_client()


def collect_all():
    all_words = collect_words()
    find_roots(all_words)
    update_db(all_words)
    connect_to_rsj()


def collect_words():
    """
    Prikuplja sve reci u svim publikacijama i smesta ih u recnik pronadjenih
    reci sa brojem pojavljivanja reci i spiskom publikacija u kojima se one
    pojavljuju.
    """
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
    """
    Konsoliduje recnik svih pronadjenih reci (words) tako sto ujedinjuje sve
    oblike iste reci pod jednu stavku, odredjenu osnovnim oblikom reci. Za
    trazenje osnovnog oblika reci kontaktira Elasticsearch servis.
    """
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
            words[oo['rec']]['korpus_id'] = oo['id']
        if index % 10000 == 0 and index > 0:
            log.info(f'Finished finding root for {index} words...')
    end_time = now()
    log.info(f'Finding roots for {total_words} words took {end_time-start_time}')


def update_db(words):
    """
    Azurira/dodaje stavke u bazu podataka na osnovu konsolidovanog recnika 
    svih pronadjenih reci u publikacijama.
    """
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
            rzo.vrsta_reci = w['vrsta']
            rzo.korpus_id = w['korpus_id']
            rzo.save()
        else:
            rzo = RecZaOdluku.objects.create(
                prvo_slovo=rec[0], 
                tekst=rec[:100], 
                vrsta_reci=w['vrsta'],
                korpus_id=w['korpus_id'],
                odluka=1, 
                broj_publikacija=len(w['pubs']), 
                broj_pojavljivanja=w['count'],
                vreme_odluke=now(),
                poslednje_generisanje=gs)
    gs.end_time = now()
    gs.save()
    end_time = now()
    log.info(f'Database updates took {end_time-start_time}')


def connect_to_rsj():
    """
    Pronalazi osnovni oblik date reci u recniku RSJ. Za uspesnu pretragu
    vraca ID te reci u recniku; za neuspesnu pretragu vraca -1.
    Preskace reci za koje je ranije vec odredjen ID iz RSJ.
    """
    start_time = now()
    log.info('Starting RSJ lookup...')
    count = 0
    for rzo in RecZaOdluku.objects.all():
        if not rzo.recnik_id and rzo.tekst:
            recnik_id = find_in_rsj(rzo.tekst, rzo.vrsta_reci)
            if recnik_id != -1:
                rzo.recnik_id = recnik_id
                rzo.save()
            count += 1
    end_time = now()
    log.info(f'RSJ lookup finished in {end_time-start_time}')


def store_word(all_words: dict, word: str, pub_id: int):
    """
    Smesta narednu rec (word) u recnik svih pronadjenih reci (all_words). 
    Azurira broj pojavljivanja reci i spisak publikacija u kojima se rec 
    pronalazi.
    """
    try:
        w = all_words[word]
        w['count'] += 1
        w['pubs'][pub_id] = pub_id
    except KeyError:
        w = {
            'tekst': word,
            'pubs': {pub_id: pub_id},
            'count': 1,
            'vrsta': None,
            'korpus_id': None,
            'recnik_id': None,
        }
        all_words[word] = w


def find_root(rec) -> list[dict]:
    """
    Pronalazi osnovni oblik date reci.
    Vraca listu recnika koji identifikuju osnovni oblik za datu leksemu. 
    Pozeljno lista ima jedan element (tada je nedvosmisleno kojoj reci 
    pripada data leksema).
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


def find_in_rsj(rec, vrsta):
    """
    Pronalazi datu rec u RSJ i vraca ID te odrednice iz RSJ, odnosno -1 ako 
    pronadjena.
    """
    resp = rsjclient.search(index='odrednica', query={'match': {'varijante': rec}})
    hitcount = len(resp['hits']['hits'])
    if hitcount == 0:
        return -1
    elif hitcount == 1:
        return resp['hits']['hits'][0]['_source']['pk']
    else:
        for hit in resp['hits']['hits']:
            if hit['_source']['vrsta'] == vrsta:
                return hit['_source']['pk']
        return -1
