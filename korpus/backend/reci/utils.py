import os
from pathlib import Path
import string

PROJECT_DIR = Path(__file__).resolve().parent.parent
NOISE_CHARS = set(string.punctuation + string.whitespace)


def get_export_basepath():
    if 'DJANGO_SETTINGS' in os.environ and os.environ['DJANGO_SETTINGS'] == 'prod':
        return '/app'
    else:
        return PROJECT_DIR


def get_export_fullpath(filename):
    return os.path.join(get_export_basepath(), 'export', filename)


def contains_only_punctuation(s):
    return all(c in NOISE_CHARS for c in s)


def clean_strings_in_dict(validated_data):
    for key, value in validated_data.items():
        if isinstance(value, str):
            if contains_only_punctuation(value):
                validated_data[key] = ''
    return validated_data


