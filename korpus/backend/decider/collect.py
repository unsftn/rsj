import logging
from django.utils.timezone import now
from decider.models import *
from indexer.cyrlat import lat_to_cyr
from indexer.search import get_es_client, get_rsj_client
from indexer.utils import remove_punctuation, contains_non_cyrillic_chars
from publikacije.models import *
from reci.models import *

log = logging.getLogger(__name__)

esclient = get_es_client()
rsjclient = get_rsj_client()


def collect_all(stdout=None):
    all_words = collect_words()
    find_roots(all_words, stdout)
    update_db(all_words, stdout)
    connect_to_rsj(stdout)


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
                    store_word(all_words, w, p.id, p.potkorpus_id)
    end_time = now()
    log.info(f'Word collection took {end_time-start_time}')
    return all_words


def find_roots(words, stdout=None):
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
        if index % 10000 == 0 and index > 0:
            if stdout:
                stdout.write(f'Finished finding root for {index} words...')
                stdout.flush()
        
        # ako ova leksema moze biti oblik vise od jedne reci, onda ne radimo
        # nista - nismo sigurni kojoj reci ona pripada
        if len(oo) == 1:
            oo = oo[0]
        else:
            continue
        
        try:
            # ako ne znamo osnovni oblik preskacemo
            if not oo['rec']:
                continue
            
            # ako je ovo rec koja jeste osnovni oblik, i vec je u mapi, 
            # ne radi nista
            if words[oo['rec']] == word:
                continue
            
            # ako je ovo rec koja nije osnovni oblik, a osnovni oblik je 
            # u mapi, akumuliraj statistike
            words[oo['rec']]['count'] += word['count']
            words[oo['rec']]['pubs'].update(word['pubs'])
            words[oo['rec']]['vrsta'] = oo['vrsta']
            words[oo['rec']]['korpus_id'] = oo['id']

            # ako je ovo rec koja nije osnovni oblik, ukloni je iz mape
            # (osnovni oblik je akumulirao njenu statistiku)
            if words[oo['rec']]['tekst'] != word['tekst']:
                del words[word['tekst']]
        except KeyError:
            # prvi put smo naisli na ovaj osnovni oblik
            # dodaj rec u mapu za ovaj osnovni oblik
            words[oo['rec']] = word
            words[oo['rec']]['vrsta'] = oo['vrsta']
            words[oo['rec']]['korpus_id'] = oo['id']

            # ako je rec razlicita od osnovnog oblika, izbaci je iz mape
            if oo['rec'] != word['tekst']:
                del words[word['tekst']]

            # tekst u reci treba da bude osnovni oblik
            word['tekst'] = oo['rec']

    end_time = now()
    log.info(f'Finding roots for {total_words} words resulted in {len(words)} entries and took {end_time-start_time}')


# def unify(words, token):
#     for key, word in list(words.items()):
#         if not key.startswith(token):
#             continue

#         oo = find_root(key)
        
#         # ako ova leksema moze biti oblik vise od jedne reci, onda ne radimo
#         # nista - nismo sigurni kojoj reci ona pripada
#         if len(oo) == 1:
#             oo = oo[0]
#         else:
#             continue
        
#         try:
#             # ako ne znamo osnovni oblik preskacemo
#             if not oo['rec']:
#                 continue
            
#             # ako je ovo rec koja jeste osnovni oblik, i vec je u mapi, 
#             # ne radi nista
#             if words[oo['rec']] == word:
#                 log.info(f'Rec {word["tekst"]} je osnovni oblik i vec je u mapi - ne radi nista')
#                 continue
            
#             # ako je ovo rec koja nije osnovni oblik, a osnovni oblik je 
#             # u mapi, akumuliraj statistike
#             log.info(f'Menjamo rec u mapi: {words[oo["rec"]]["tekst"]} {words[oo["rec"]]["count"]} {len(words[oo["rec"]]["pubs"])}')
#             words[oo['rec']]['count'] += word['count']
#             words[oo['rec']]['pubs'].update(word['pubs'])
#             words[oo['rec']]['vrsta'] = oo['vrsta']
#             words[oo['rec']]['korpus_id'] = oo['id']
#             log.info(f'Akumulirane statistike: {words[oo["rec"]]["tekst"]} {words[oo["rec"]]["count"]} {len(words[oo["rec"]]["pubs"])} iz reci: {word["tekst"]} {word["count"]} {len(word["pubs"])}')

#             # ako je ovo rec koja nije osnovni oblik, ukloni je iz mape
#             # (osnovni oblik je akumulirao njenu statistiku)
#             if words[oo['rec']]['tekst'] != word['tekst']:
#                 log.info(f'Rec {word["tekst"]} nije osnovni oblik, uklanjamo je iz mape')
#                 del words[word['tekst']]
#         except KeyError:
#             # prvi put smo naisli na ovaj osnovni oblik
#             # dodaj rec u mapu za ovaj osnovni oblik
#             words[oo['rec']] = word
#             words[oo['rec']]['vrsta'] = oo['vrsta']
#             words[oo['rec']]['korpus_id'] = oo['id']
#             log.info(f'Rec {word["tekst"]} prvi put smo naisli na ovaj osnovni oblik, dodajemo je u mapu')

#             # ako je rec razlicita od osnovnog oblika, izbaci je iz mape
#             if oo['rec'] != word['tekst']:
#                 log.info(f'Rec {word["tekst"]} se razlikuje od osnovnog oblika {oo["rec"]}, izbacujemo je iz mape')
#                 del words[word['tekst']]

#             # tekst u reci treba da bude osnovni oblik
#             log.info(f'Tekst u reci {word["tekst"]} postavljamo na osnovni oblik: {oo["rec"]}')
#             word['tekst'] = oo['rec']


def update_db(words, stdout=None):
    """
    Azurira/dodaje stavke u bazu podataka na osnovu konsolidovanog recnika 
    svih pronadjenih reci u publikacijama.
    """
    start_time = now()
    log.info('Started database updates...')
    gs = GenerisaniSpisak.objects.create(start_time=now())
    for i, (k, w) in enumerate(words.items()):
        rec = k
        rzos = RecZaOdluku.objects.filter(tekst=rec)
        p1 = 1 in w['potkorpus']
        p2 = 2 in w['potkorpus']
        p3 = 3 in w['potkorpus']
        p4 = 4 in w['potkorpus']
        p5 = 5 in w['potkorpus']
        p6 = 6 in w['potkorpus']
        p7 = 7 in w['potkorpus']
        p8 = 8 in w['potkorpus']
        p9 = 9 in w['potkorpus']
        if len(rzos) > 0:
            rzo = rzos[0]
            rzo.broj_publikacija = len(w['pubs'])
            rzo.broj_pojavljivanja = w['count']
            rzo.poslednje_generisanje = gs
            rzo.vrsta_reci = w['vrsta']
            rzo.korpus_id = w['korpus_id']
            if p1:
                rzo.potkorpus_1 = True
            if p2:
                rzo.potkorpus_2 = True
            if p3:
                rzo.potkorpus_3 = True
            if p4:
                rzo.potkorpus_4 = True
            if p5:  
                rzo.potkorpus_5 = True
            if p6:
                rzo.potkorpus_6 = True
            if p7:
                rzo.potkorpus_7 = True
            if p8:
                rzo.potkorpus_8 = True
            if p9:
                rzo.potkorpus_9 = True
            rzo.save()
        else:
            prvo_slovo = 'X' if contains_non_cyrillic_chars(rec) else rec[0]
            rzo = RecZaOdluku.objects.create(
                prvo_slovo=prvo_slovo, 
                tekst=rec[:100], 
                vrsta_reci=w['vrsta'],
                korpus_id=w['korpus_id'],
                odluka=1, 
                broj_publikacija=len(w['pubs']), 
                broj_pojavljivanja=w['count'],
                vreme_odluke=now(),
                potkorpus_1=p1,
                potkorpus_2=p2,
                potkorpus_3=p3,
                potkorpus_4=p4,
                potkorpus_5=p5,
                potkorpus_6=p6,
                potkorpus_7=p7,
                potkorpus_8=p8,
                potkorpus_9=p9,
                poslednje_generisanje=gs)
        if i % 10000 == 0 and i > 0:
            if stdout:
                stdout.write(f'Saved {i} words...')
                stdout.flush()
    gs.end_time = now()
    gs.save()
    end_time = now()
    log.info(f'Database updates took {end_time-start_time}')


def connect_to_rsj(stdout=None):
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
            recnik_id, vrsta, status = find_in_rsj(rzo.tekst, rzo.vrsta_reci)
            if recnik_id != -1:
                rzo.recnik_id = recnik_id
                if not rzo.vrsta_reci:
                    rzo.vrsta_reci = vrsta
                rzo.save()
        count += 1
        if count % 10000 == 0:
            if stdout:
                stdout.write(f'Lookup done for {count} words...')
                stdout.flush()
    end_time = now()
    log.info(f'RSJ lookup finished in {end_time-start_time}')


def store_word(all_words: dict, word: str, pub_id: int, potkorpus_id: int):
    """
    Smesta narednu rec (word) u recnik svih pronadjenih reci (all_words). 
    Azurira broj pojavljivanja reci i spisak publikacija u kojima se rec 
    pronalazi.
    """
    try:
        w = all_words[word]
        w['count'] += 1
        w['pubs'][pub_id] = pub_id
        w['potkorpus'] |= set([potkorpus_id])
    except KeyError:
        w = {
            'tekst': word,
            'pubs': {pub_id: pub_id},
            'count': 1,
            'vrsta': None,
            'korpus_id': None,
            'recnik_id': None,
            'potkorpus': set([potkorpus_id])
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
    pronadjena. Druga komponenta tuple je vrsta reci iz RSJ (ako je pronadjena).
    """
    resp = rsjclient.search(index='odrednica', query={'match': {'varijante': rec}})
    hitcount = len(resp['hits']['hits'])
    if hitcount == 0:
        return -1, None, None
    elif hitcount == 1:
        item = resp['hits']['hits'][0]['_source']
        return item['pk'], item['vrsta'], int(item['status'])
    else:
        for hit in resp['hits']['hits']:
            if vrsta is not None and hit['_source']['vrsta'] == vrsta:
                return hit['_source']['pk'], vrsta, int(hit['_source']['status'])
        return -1, None, None
