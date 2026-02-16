import logging
import requests as http_requests
from django.conf import settings

log = logging.getLogger(__name__)

WORD_TYPE_TO_INT = {
    'imenica': 0, 'glagol': 1, 'pridev': 2, 'prilog': 3,
    'predlog': 4, 'zamenica': 5, 'uzvik': 6, 'recca': 7,
    'veznik': 8, 'broj': 9,
}


def _word_type_to_int(word_type_str):
    return WORD_TYPE_TO_INT.get(word_type_str, 10)


def find_root(rec) -> list[dict]:
    """
    Pronalazi osnovni oblik date reci.
    Vraca listu recnika koji identifikuju osnovni oblik za datu leksemu.
    Pozeljno lista ima jedan element (tada je nedvosmisleno kojoj reci
    pripada data leksema).
    """
    try:
        url = f'{settings.SEARCH_ENGINE_URL}/morphology/form/{rec}'
        resp = http_requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        retval = []
        for entry in data.get('results', []):
            original_id = entry.get('original_id')
            if original_id is None:
                continue
            vrsta = _word_type_to_int(entry['word_type'])
            retval.append({
                'rec': entry['base_form'],
                'pk': f'{vrsta}_{original_id}',
                'vrsta': vrsta,
                'id': original_id,
            })
        return retval
    except Exception as error:
        log.error(f'Rust engine find_root error: {error}')
        return []


def find_in_rsj(rec, vrsta):
    """
    Pronalazi datu rec u RSJ i vraca ID te odrednice iz RSJ, odnosno -1 ako
    nije pronadjena. Druga komponenta tuple je vrsta reci iz RSJ (ako je
    pronadjena). Treca komponenta je status (podrazumevano 0 jer Rust engine
    ne cuva status).
    """
    try:
        url = f'{settings.SEARCH_ENGINE_URL}/odrednica/prefix/{rec}'
        resp = http_requests.get(url, params={'limit': 100})
        resp.raise_for_status()
        data = resp.json()
        results = data.get('results', [])
        if not results:
            return -1, None, None

        # Filter for exact match (the prefix search may return extra results)
        exact_matches = [r for r in results if rec in r.get('rec', '')]
        if not exact_matches:
            # Fall back: check if any variant matches
            exact_matches = results

        if len(exact_matches) == 1:
            item = exact_matches[0]
            return item['original_id'], item['vrsta'], 0
        else:
            for item in exact_matches:
                if vrsta is not None and item['vrsta'] == vrsta:
                    return item['original_id'], item['vrsta'], 0
            return -1, None, None
    except Exception as error:
        log.error(f'Rust engine find_in_rsj error: {error}')
        return -1, None, None
