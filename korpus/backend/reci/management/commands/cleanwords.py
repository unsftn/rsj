from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from ...models import *
from ...utils import contains_only_punctuation

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Cisti djubre u unetim recima - ako neko polje ima samo interpunkciju'

    def handle(self, *args, **options):
        start_time = datetime.now()
        log.info('Ciscenje reci...')
        self.clean_words(Imenica.objects.all())
        self.clean_words(Glagol.objects.all())
        self.clean_words(Pridev.objects.all())
        self.clean_words(Prilog.objects.all())
        self.clean_words(Zamenica.objects.all())
        self.clean_words(Predlog.objects.all())
        self.clean_words(Veznik.objects.all())
        self.clean_words(Uzvik.objects.all())
        self.clean_words(Recca.objects.all())
        self.clean_words(Broj.objects.all())
        end_time = datetime.now()
        log.info(f'Ciscenje reci trajalo {str(end_time-start_time)}')

    def clean_words(self, words):
        for w in words:
            changed = self.clean_dict(w.__dict__)
            if changed:
                w.save()
                log.info(f'Ciscenje reci: {w.osnovni_oblik()}')

    def clean_dict(self, d):
        changed = False
        for key, value in d.items():
            if isinstance(value, str):
                if contains_only_punctuation(value):
                    d[key] = ''
                    changed = True
            elif isinstance(value, list):
                changed |= self.clean_dict(value)
        return changed
