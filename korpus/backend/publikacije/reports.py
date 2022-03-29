from .models import *
from .utils import *


def all_words_from_all_pubs():
    words = {}
    for pub in Publikacija.objects.all():
        pub_words = all_words_from_pub(pub)
        words.update(pub_words)
    return words


def all_words_from_pub(pub):
    words = {}
    try:
        tekst = TekstPublikacije.objects.filter(publikacija=pub).order_by('redni_broj')
        for t in tekst:
            page_text = t.tekst
            parsed_words = parse_to_words(page_text)
            for w in parsed_words:
                w = w.lower()
                entry = {
                    'pubid': pub.id,
                    'pubskr': pub.skracenica,
                    'pages': [tekst.redni_broj]
                }
                if words.get(w):
                    if words[w].get(pub.id):
                        words[w][pub.id]['pages'].append(tekst.redni_broj)
                    else:
                        words[w][pub.id] = entry
                else:
                    words[w] = {pub.id: entry}
    except TekstPublikacije.DoesNotExist:
        return {}


def parse_to_words(text):
    text = remove_punctuation(text)
    words = text.split()
    return [w for w in words if len(w) > 0]
