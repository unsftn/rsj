from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from ...utils import get_export_fullpath
from ...morphimport import wikimorph_import

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import Wikimorph-sr file'

    def add_arguments(self, parser):
        parser.add_argument('--filename', type=str, help='File to import')
        parser.add_argument('--gzip', action='store_true')

    def handle(self, *args, **options):
        start_time = datetime.now()
        filename = options.get('filename')
        gzip = options.get('gzip')
        file_path = get_export_fullpath(filename)
        wikimorph_import(file_path, gzip)
        end_time = datetime.now()
        log.info(f'Import trajao ukupno {str(end_time-start_time)}')
