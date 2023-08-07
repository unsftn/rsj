import logging
import re
from odrednice.models import Odrednica, Znacenje, Podznacenje

log = logging.getLogger(__name__)


def strip_dot(text):
    text = text.strip()
    if text.endswith('.'):
        text = text[:-1]
    return text


def parse_file(filename):
    """
    Cita txt fajl jednotomnika i sastavlja odrednice koje se protezu u 
    potencijalno vise redova, razdvojene bar jednim praznim redom.
    
    Parameters:
        filename (str): naziv fajla iz koga se citaju odrednice

    Returns
        dict: recnik sa glavom odrednice kao kljucem i celim tekstom odrednice kao vrednoscu
    """
    entries = {}
    with open(filename, 'r') as infile:
        entry_text = ''
        for line in infile.readlines():
            line = line.strip()
            if len(line) < 2:
                if not entry_text:
                    continue
                head = entry_text.split()[0]
                if head.endswith(','):
                    head = head[:-1]
                entries[head] = entry_text.strip()
                entry_text = ''
            else:
                entry_text += line.strip() + ' '
    return entries


def multiple_submeanings(text):
    """ 
    Parsira podznacenja u datom tekstu. Tekst predstavlja celokupan sadrzaj 
    jednog znacenja, koje moze imati svoj sadrzaj pre nego sto pocnu podznacenja.

    Parameters:
        text (str): tekst znacenja
      
    Returns:
        list<str>: tekstovi podznacenja
    """
    retval = []
    pattern = re.compile(r'(^|\s)[а-ш]\. ')
    match = pattern.search(text)
    while match:
        start = match.end()
        match = pattern.search(text, match.end())
        if match:
            end = match.start()
            retval.append(strip_dot(text[start:end]))
        else:
            retval.append(strip_dot(text[start:]))
    return retval


def multiple_meanings(text):
    """ 
    Parsira znacenja u datom tekstu. Tekst predstavlja celokupan sadrzaj 
    odrednice koji ima bar dva znacenja.

    Parameters:
        text (str): tekst odrednice
    
    Returns:
        list<str>: lista parsiranih znacenja (mozda imaju podznacenja u sebi)
    """
    rex = re.findall(r'(\d{1,2}\.) (([^\d])*)', text)
    meanings = [strip_dot(r[1]) for r in rex]
    return meanings


def parse_meanings(entries):
    """
    Parsira tekst odrednice, pazeci na broj znacenja i podznacenja.

    Parameters:
        entries (dict): recnik sa odrednicama: kljuc je glava, vrednost je tekst odrednice

    Returns:
        dict: recnik sa odrednicama: kljuc je glava, vrednost je recnik sa kljucevima key (str) i meanings (list<dict>)
    """
    retval = {}
    for key, entry_text in entries.items():
        entry = {'key': key, 'meanings': []}
        if ' 1. ' in entry_text:  # ima vise znacenja
            meaning_texts = multiple_meanings(entry_text)
            for meaning in meaning_texts:
                if ' б. ' in meaning:  # ima podznacenja
                    submeanings = multiple_submeanings(meaning)
                    if meaning.startswith('а.'):
                        meaning = ''
                else:
                    submeanings = []
                entry['meanings'].append({'text': meaning, 'submeanings': submeanings})
        else:  # ima jedno znacenje
            pieces = entry_text.split()
            if not pieces:
                continue
            start = 1
            if pieces[0].endswith(','):  # ima nastavke
                while start < len(pieces) and pieces[start].startswith('-'):  # preskoci nastavke
                    start += 1
            while start < len(pieces) and (pieces[start].endswith('.') or len(pieces[start]) < 3):
                start += 1
            text = ' '.join(pieces[start:])
            entry['meanings'] = [{'text': text, 'submeanings': []}]
        retval[key] = entry
    return retval


def process_file(filename):
    """
    Ucitava znacenja odrednica iz tekstualnog fajla jednotomnika.

    Parameters:
        filename (str): naziv fajla sa sadrzajem jednotomnika

    Returns:
        dict: recnik sa odrednicama: kljuc je glava, vrednost je recnik sa kljucevima key (str) i meanings (list<dict>)
    """
    entries1 = parse_file(filename)
    entries2 = parse_meanings(entries1)
    return entries2


def import_entries(entries):
    """ 
    Upisuje (prethodno procitana) znacenja i podznacenja u bazu, samo za 
    odrednice koje nemaju svojih znacenja i podznacenja.

    Parameters:
        entries (dict<str,dict>): recnik sa odrednicama: kljuc je glava, vrednost je recnik sa kljucevima key (str) i meanings (list<dict>)

    Returns
        int, int, int: broj izmenjenih odrednica, dodatih znacenja, dodatih podznacenja
    """
    count_znacenje = 0
    count_podznacenje = 0
    count_odrednica = 0
    for key, entry in entries.items():
        try:
            odrednica = Odrednica.objects.get(sortable_rec=key)
            if odrednica.znacenje_set.count() == 0:
                count_odrednica += 1
                for index, meaning in enumerate(entry['meanings']):
                    znacenje = Znacenje.objects.create(odrednica=odrednica, tekst=meaning['text'][:2000], redni_broj=index+1)
                    count_znacenje += 1
                    for index2, submeaning in enumerate(meaning['submeanings']):
                        Podznacenje.objects.create(znacenje=znacenje, tekst=submeaning[:2000], redni_broj=index2+1)
                        count_podznacenje += 1
            else:
                log.info(f'Odrednica {key} vec ima uneta znacenja')
        except Odrednica.DoesNotExist:
            log.info(f'Nije pronadjena odrednica: {key}')
        except Odrednica.MultipleObjectsReturned:
            log.info(f'Odrednica pronadjena vise puta: {key}')
    return count_odrednica, count_znacenje, count_podznacenje


if __name__ == '__main__':
    entries = process_file('jednotomnik.txt')
    import_entries(entries)
