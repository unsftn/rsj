import logging
from publikacije.models import *
from reci.models import *
from indexer.cyrlat import lat_to_cyr
from indexer.search import find_osnovni_oblik
from indexer.utils import remove_punctuation

log = logging.getLogger(__name__)


def collect_all():
    # TODO: create new GenerisaniSpisak
    all_words = collect_words()
    update_db(all_words)


def collect_words():
    all_words = {}
    log.info('Started word collection...')
    for p in Publikacija.objects.all():
        new_pub = True  # TODO: FIGURE THIS OUT
        for tekst in TekstPublikacije.objects.all():
            content = remove_punctuation(lat_to_cyr(tekst.tekst.lower()))
            for w in content.split():
                store_word(all_words, w, new_pub)

    # TODO: for each publication, for each text, for each word
    # - convert to cyrillic
    # - find root word if any
    # - put in a dict
    # - update pub_counter, freq_counter
    # return dict
    log.info('Word collection done.')


def update_db(words):
    log.info('Started database updates...')
    # TODO: for each word in dict
    # - find word in RecZaOdluku
    # - if found: update generation_date
    # - else: add new entry
    log.info('Database updates done.')


def store_word(all_words: dict, word: str, new_publication: bool):
    oo = find_osnovni_oblik(word)
    if len(oo) == 1:
        oo = oo['rec']
    else:
        oo = word

    try:
        w = all_words[oo]
        w['broj_pojavljivanja'] += 1
        if new_publication:
            w['broj_publikacija'] += 1
    except KeyError:
        w = {
            'tekst': oo,
            'broj_publikacija': 1,
            'broj_pojavljivanja': 1
        }
        all_words[oo] = w
