import logging
import unicodedata as ud
from django.core.management.base import BaseCommand
from odrednice.models import Odrednica
from odrednice.text import remove_punctuation
from pretraga.cyrlat import lat_to_cyr

log = logging.getLogger(__name__)

cyrillic_letters = {}


class Command(BaseCommand):
    help = 'List entries that contain non-cyrillic characters'

    def handle(self, *args, **options):
        self.style.NOTICE(f'Listanje svih reči koje sadrže ne-ćirilične znakove')
        log.info('Listanje svih reči koje sadrze ne-ćirilične znakove')

        odrednice = Odrednica.objects.all()
        bad_word_count = 0
        for odr in odrednice:
            clean = remove_punctuation(odr.rec).replace(' ', '')
            bad_chars = check_non_cyrillic(clean)
            if bad_chars:
                bad_word_count += 1
                odr.rec = lat_to_cyr(odr.rec)
                odr.save()
                log.info(f'Reč {odr.rec} ({odr.id}) sadži ne-ćiriličke znake: {bad_chars}')
            
        self.style.SUCCESS(f'Pronađeni ne-ćirilični znakovi u {bad_word_count} reči.')
        log.info(f'Pronađeni ne-ćirilični znakovi u {bad_word_count} reči.')


def is_cyrillic(char):
    try:
        return cyrillic_letters[char]
    except KeyError:
        return cyrillic_letters.setdefault(char, 'CYRILLIC' in ud.name(char))


def only_cyrillic_chars(text):
    return all(is_cyrillic(char) for char in text if char.isalpha())


def check_non_cyrillic(text):
    retval = []
    for char in text:
        if not 'CYRILLIC' in ud.name(char):
            retval.append(char)
    return retval