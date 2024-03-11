import os
import logging
from django.conf import settings
import textract
from .models import FajlPublikacije

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
    try:
        text = textract.process(filepath).decode('utf-8')
    except Exception as e:
        logger.error(f'Greška pri ekstrakciji teksta iz fajla: {filepath}')
        logger.error(e)
        return None
    return text
    # files = {'file': open(filepath, 'rb')}
    # response = requests.post('https://extractor.rsj.rs/extract', files=files)
    # logger.info(f'Status ekstrakcije: {response.status_code}')
    # return response.json()
