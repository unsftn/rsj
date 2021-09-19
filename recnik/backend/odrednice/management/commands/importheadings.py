import logging
from django.core.management.base import BaseCommand
import docx
from odrednice.models import Odrednica
from odrednice.text import remove_punctuation

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import headings from a Word file'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='Word file with headings')

    def handle(self, *args, **options):
        file = options.get('file')
        log.info(f'Import glava iz fajla {file}')
        word_count = 0
        try:
            document = docx.Document(file)
            for para in document.paragraphs:
                word = ''
                for run in para.runs:
                    font_name = run.font.name
                    if not font_name:
                        word += run.text
                    elif font_name == 'Bg knjiga':
                        word += run.text
                    elif font_name == 'Bg knjiga 01':
                        word += add_accent(run.text, '̀')
                    elif font_name == 'Bg knjiga 02':
                        word += add_accent(run.text, '́')
                    elif font_name == 'Bg knjiga 03':
                        word += add_accent(run.text, '̏')
                    elif font_name == 'Bg knjiga 04':
                        word += add_accent(run.text, '̑')
                    elif font_name == 'Bg knjiga 05':
                        word += add_accent(run.text, '̄')
                has_se = word.find('(се)') > -1
                if has_se:
                    word = word.replace('(се)', '')
                word = word.strip()
                try:
                    Odrednica.objects.get(rec=word)
                except Odrednica.DoesNotExist:
                    clean = remove_punctuation(word)
                    vrsta = 0
                    if clean.endswith('ти'):
                        vrsta = 1
                    elif clean.endswith('ски') or clean.endswith('шки') or clean.endswith('чки'):
                        vrsta = 2
                    Odrednica.objects.create(rec=word, vrsta=vrsta, opciono_se=has_se)
                    word_count += 1
        except Exception as ex:
            log.fatal(ex)

        self.style.SUCCESS(f'Zavrsen import {word_count} glava.')
        log.info(f'Zavrsen import {word_count} glava.')


def add_accent(text, accent_char):
    retval = ''
    for ch in text:
        retval += ch + accent_char
    return retval
