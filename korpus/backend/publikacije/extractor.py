import os
import logging
from django.conf import settings
import requests
from .models import FajlPublikacije, TekstPublikacije

logger = logging.getLogger(__name__)


def extract_file(fajl_publikacije):
    if isinstance(fajl_publikacije, int):
        try:
            fajl_publikacije = FajlPublikacije.objects.get(id=fajl_publikacije)
        except FajlPublikacije.DoesNotExist:
            return None
    if not isinstance(fajl_publikacije, FajlPublikacije):
        return None
    filepath = os.path.join(settings.MEDIA_ROOT, fajl_publikacije.filepath())
    files = {'file': open(filepath, 'rb')}
    response = requests.post('https://extractor.rsj.rs/extract', files=files)
    logger.info(f'Status ekstrakcije: {response.status_code}')
    return response.json()
