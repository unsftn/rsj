import re
from odrednice.text import remove_punctuation
from .cyrlat import cyr_to_lat

REGEX_CONTAINS_PARENTHESES = re.compile('(.+)\\((.*?)\\)(.*?)')


def clear_text(obj):
    if not obj:
        return obj
    if isinstance(obj, str):
        if not REGEX_CONTAINS_PARENTHESES.match(obj):
            return remove_punctuation(obj)
        else:
            return [remove_punctuation(REGEX_CONTAINS_PARENTHESES.sub('\\1\\3', obj)), remove_punctuation(REGEX_CONTAINS_PARENTHESES.sub('\\1\\2\\3', obj))]
    if isinstance(obj, list):
        new_list = []
        for item in obj:
            if isinstance(item, str):
                if not REGEX_CONTAINS_PARENTHESES.match(item):
                    new_list.append(remove_punctuation(item))
                else:
                    new_list.append(remove_punctuation(REGEX_CONTAINS_PARENTHESES.sub('\\1\\3', item)))
                    new_list.append(remove_punctuation(REGEX_CONTAINS_PARENTHESES.sub('\\1\\2\\3', item)))
            else:
                new_list.append(item)
        return new_list
    return obj


def add_latin(lst):
    result = []
    result.extend(lst)
    for item in lst:
        result.append(cyr_to_lat(item))
    return result


def append_latin(tekst):
    return tekst + ' ' + cyr_to_lat(tekst)
