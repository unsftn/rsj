import unicodedata

from .cyrlat import is_cyrillic
from .models import FajlPublikacije


def renumber_files(pub_id):
    files = FajlPublikacije.objects.filter(publikacija_id=pub_id).order_by('redni_broj')
    for i, f in enumerate(files):
        f.redni_broj = i + 1
        f.save()


def remove_punctuation(text):
    cleared_text = ''.join(c for c in text if unicodedata.category(c) in ['Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'NI', 'Zs'])
    return cleared_text


def get_autori(publikacija):
    if publikacija.autor_set.count() == 0:
        return ''
    autori = []
    for aut in publikacija.autor_set.all().order_by('redni_broj'):
        if aut.prezime:
            if aut.ime:
                autori.append(f'{aut.prezime}, {aut.ime}')
            else:
                autori.append(f'{aut.prezime}')
        else:
            if aut.ime:
                autori.append(f'{aut.ime}')
    if not autori:
        return ''
    retval = ', '.join(autori)
    if retval[-1] != '.':
        retval += '.'
    return retval


def get_opis_monografske(publikacija):
    autori = get_autori(publikacija)
    opis = autori + (' ' if autori else '') + f'<i>{publikacija.naslov}</i>'
    if publikacija.tom:
        opis += f', {publikacija.tom}'
    prev = 'прев' if is_cyrillic(publikacija.naslov) else 'prev'
    if publikacija.prevodilac:
        opis += f', {prev}. {publikacija.prevodilac}'
    if len(opis) > 0 and opis[-1] != '.':
        opis += '.'
    if publikacija.izdavac:
        if len(opis) > 0:
            opis += f' {publikacija.izdavac}'
        if publikacija.godina:
            opis += f', {publikacija.godina}'
    elif publikacija.godina:
        if len(opis) > 0:
            opis += f' {publikacija.godina}'
        else:
            opis = f'{publikacija.godina}'
    if len(opis) > 0 and opis[-1] != '.':
        opis += '.'
    return opis


def get_opis_periodika(publikacija):
    if publikacija.izdavac:
        if publikacija.godina:
            return f'<i>{publikacija.izdavac}</i>, {publikacija.godina}.'
        else:
            return f'{publikacija.izdavac}.'
    else:
        if publikacija.godina:
            return f'{publikacija.godina}.'


def get_opis_publikacije(publikacija):
    opis = ''
    if publikacija.potkorpus.id == 1:
        # knjizevni korpus
        opis = get_opis_monografske(publikacija)
    elif publikacija.potkorpus.id == 2:
        # novinski
        opis = get_opis_periodika(publikacija)
    elif publikacija.potkorpus.id == 3:
        # razgovorni
        opis = get_opis_periodika(publikacija) + ' (YouTube)'
    elif publikacija.potkorpus.id == 4:
        # naucni
        if publikacija.izdavac == 'Српска енциклопедија':
            opis = f'<i>Српска енциклопедија</i>. Нови Сад: Матица српска, 2024.'
        else:
            opis = get_opis_monografske(publikacija)
    elif publikacija.potkorpus.id == 5:
        # administrativni
        opis = f'<i>{publikacija.naslov}</i>, {publikacija.izdavac}'
        if publikacija.godina:
            opis += f', {publikacija.godina}'
        if len(opis) > 0 and opis[-1] != '.':
            opis += '.'
    return opis
