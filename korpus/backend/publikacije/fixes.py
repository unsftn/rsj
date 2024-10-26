import logging
import re
from publikacije.models import *
from publikacije.cyrlat import cyr_to_lat, lat_to_cyr

log = logging.getLogger(__name__)


SKRACENICE = {
    'Automagazin': 'Аутомаг',
    'Auto republika': 'Аутореп',
    'hotsport.rs': 'Хот',
    'Južne Vesti': 'Јуж',
    'Lepota i zdravlje': 'Леп',
    'NIN': 'НИН',
    'Nova ekonomija': 'Н. Еко',
    'Vreme': 'Вре',
    'Pecat': 'Печ',
    'Peščanik': 'Пешч',
    'Sportske.net': 'Спо',
    'Politika': 'Пол',
    'Polikin zabavnik': 'П. Заб',
    'Centar za antiautoritarne studije': 'ЦАС',
    'Biznis priče': 'Биз. пр',
    'Novi standard': 'Н. станд',
    'Agelast': 'Агел',
    'Catena mundi': 'Кат. мунд',
    'Dva i po psihijatra': '2,5 псих',
    'Oko magazin': 'Око. маг',
    'Još podkast jedan': 'Још. подк',
    'Ivan Kosogor podcast': 'Ив. Кос',
    'Drugačiji fitness': 'Друг. фит',
    'Pojačalo podcast': 'Пој. подк',
    'RTS Ordinacija': 'РТС Орд',
    'RTS Kvadratura kruga': 'РТС Квад',
    'RTS Oko': 'РТС Око',
    'Da sam ja neko': 'Да сам',
    'Rubikon': 'Рубик',
    'Lukavstvo uma': 'Лук. ума',
}


def get_next_rbr(prefiks_skracenice):
    """
    Poslednji redni broj za dati prefiks skracenice se cuva u bazi podataka.
    """
    poslednji = PoslednjiRedniBroj.objects.filter(prefiks_skracenice=prefiks_skracenice).first()
    if poslednji:
        poslednji.redni_broj += 1
        poslednji.save()
        rbr = poslednji.redni_broj
        return rbr
    else:
        PoslednjiRedniBroj.objects.create(prefiks_skracenice=prefiks_skracenice, redni_broj=1)
        return 1


def print_poslednji_rbr():
    for poslednji in PoslednjiRedniBroj.objects.all():
        print(f'{poslednji.prefiks_skracenice}: {poslednji.redni_broj}')


def razmak_posle_tacke(skracenica):
    """
    Dodaje razmak posle tacke u skracenici.
    """
    result = re.sub(r'\.(\S)', r'. \1', skracenica)
    return result


def fix_skracenice():
    for izvor in Publikacija.objects.all():
        if izvor.skracenica not in ['-', '']:
            if izvor.potkorpus_id == 1:
                original = izvor.skracenica
                cirilica = lat_to_cyr(original)
                if izvor.skracenica != cirilica:
                    izvor.skracenica = cirilica
                    izvor.save()
            original = izvor.skracenica
            sa_razmakom = razmak_posle_tacke(original)
            if original != sa_razmakom:
                izvor.skracenica = sa_razmakom
                izvor.save()
        else:
            if izvor.izdavac is None:
                continue
            skr = SKRACENICE.get(izvor.izdavac)
            if not skr:
                log.warning(f'Nepoznata skraćenica za izvor {izvor.izdavac}, publikacija {izvor.id}')
            godina = izvor.godina if izvor.godina else ''
            if izvor.potkorpus_id in [2, 3]:  # novinski ili razgovorni
                prefiks_skracenice = f'{skr}. {godina}' if godina else skr
                rbr = get_next_rbr(prefiks_skracenice)
                skracenica = f'{prefiks_skracenice}. {rbr}'
                izvor.skracenica = skracenica
                izvor.save()
            elif izvor.potkorpus_id == 4:  # naucni
                if izvor.izdavac == 'Српска енциклопедија':
                    izvor.skracenica = 'СЕ'
                    izvor.save()
            elif izvor.potkorpus_id == 5:  # administrativni
                if izvor.izdavac == 'Paragraf':
                    prefiks_skracenice = 'ПЛ'
                    rbr = get_next_rbr(prefiks_skracenice)
                    skracenica = f'{prefiks_skracenice}. {rbr}'
                    izvor.skracenica = skracenica
                    izvor.save()


def fix_poslednji_brojevi():
    for poslednji in PoslednjiRedniBroj.objects.all():
        original = poslednji.prefiks_skracenice
        sa_razmakom = razmak_posle_tacke(original)
        if original != sa_razmakom:
            poslednji.prefiks_skracenice = sa_razmakom
            poslednji.save()

