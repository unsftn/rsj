import os
import logging
from django.conf import settings
from pdfminer.high_level import extract_text
import docx2txt
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
        if filepath.endswith('.pdf'):
            text = extract_text(filepath)
        elif filepath.endswith('.docx'):
            text = docx2txt.process(filepath)
        else:
            text = ''
    except Exception as e:
        logger.error(f'Greška pri ekstrakciji teksta iz fajla: {filepath}')
        logger.error(e)
        return None
    return text
