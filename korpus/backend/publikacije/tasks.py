import logging
import os
from django.db.models import Max
from .extractor import extract_file
from .processing import extract_pdf_file, get_filter, invoke_filter, get_filter_list
from .models import *

log = logging.getLogger(__name__)


def extract_text_for_pub(pub_id):
    try:
        publikacija = Publikacija.objects.get(id=pub_id)
        TekstPublikacije.objects.filter(publikacija=publikacija).delete()
        for fajl_publikacije in publikacija.fajlpublikacije_set.all().order_by('redni_broj'):
            filepath = fajl_publikacije.filepath()
            name, ext = os.path.splitext(filepath)
            if ext.lower().startswith('.pdf'):
                pages = extract_pdf_file(filepath)
            elif ext.lower().startswith('.doc'):
                extract = extract_file(fajl_publikacije)
                pages = [page['text'] for page in extract['pages']]
            else:
                log.fatal(f'Unsuported file format for: {filepath}')
                return
            prethodni = TekstPublikacije.objects.filter(publikacija_id=pub_id).aggregate(Max('redni_broj'))[
                            'redni_broj__max'] or 0
            for index, page in enumerate(pages):
                TekstPublikacije.objects.create(
                    publikacija_id=pub_id,
                    redni_broj=prethodni + index + 1,
                    tekst=page,
                    tagovan_tekst='')
    except Publikacija.DoesNotExist as ex:
        log.fatal(ex)
