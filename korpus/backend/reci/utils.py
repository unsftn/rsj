import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent


def get_export_basepath():
    if 'DJANGO_SETTINGS' in os.environ and os.environ['DJANGO_SETTINGS'] == 'prod':
        return '/app'
    else:
        return PROJECT_DIR


def get_export_fullpath(filename):
    return os.path.join(get_export_basepath(), 'export', filename)
