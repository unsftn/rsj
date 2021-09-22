import logging
import os
from django.core.management.base import BaseCommand, CommandError
import docx
from odrednice.models import Odrednica

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import headings from a Word file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Word file with headings')

    def handle(self, *args, **options):
        file = options.get('file')
        if not os.path.exists(file):
            raise CommandError(f'File {file} does not exist.')
        log.info(f'Import glava iz fajla {file}')
        word_count = 0
        try:
            document = docx.Document(file)
            for para in document.paragraphs:
                word = ''
                rbr_homo = None
                for run in para.runs:
                    font_name = run.font.name
                    if run.font.superscript:
                        try:
                            rbr_homo = int(run.text)
                        except:
                            pass
                    elif not font_name:
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
                    if rbr_homo:
                        Odrednica.objects.get(rec=word, rbr_homonima=rbr_homo)
                    else:
                        Odrednica.objects.get(rec=word)
                except Odrednica.DoesNotExist:
                    Odrednica.objects.create(rec=word, vrsta=10, rbr_homonima=rbr_homo, opciono_se=has_se)
                    word_count += 1
        except Exception as ex:
            log.fatal(ex)

        log.info(f'Zavrsen import {word_count} glava.')


def add_accent(text, accent_char):
    retval = ''
    for ch in text:
        retval += ch + accent_char
    return retval
