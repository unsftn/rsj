CYRILLIC_CHARS = [
    '\u0410', '\u0411', '\u0412', '\u0413',
    '\u0414', '\u0402', '\u0415', '\u0416', '\u0417', '\u0418',
    '\u0408', '\u041A', '\u041B', '\u041C', '\u041D', '\u041E',
    '\u041F', '\u0420', '\u0421', '\u0422', '\u040B', '\u0423',
    '\u0424', '\u0425', '\u0426', '\u0427', '\u0428', '\u0430',
    '\u0431', '\u0432', '\u0433', '\u0434', '\u0452', '\u0435',
    '\u0436', '\u0437', '\u0438', '\u0458', '\u043A', '\u043B',
    '\u043C', '\u043D', '\u043E', '\u043F', '\u0440', '\u0441',
    '\u0442', '\u045B', '\u0443', '\u0444', '\u0445', '\u0446',
    '\u0447', '\u0448']

LATIN_CHARS = [
    'A', 'B', 'V', 'G', 'D', '\u0110', 'E',
    '\u017D', 'Z', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S',
    'T', '\u0106', 'U', 'F', 'H', 'C', '\u010C', '\u0160', 'a', 'b',
    'v', 'g', 'd', '\u0111', 'e', '\u017e', 'z', 'i', 'j', 'k', 'l',
    'm', 'n', 'o', 'p', 'r', 's', 't', '\u0107', 'u', 'f', 'h', 'c',
    '\u010d', '\u0161'
]

AZBUKA = 'абвгдђежзијклљмнњопрстћуфхцчџш'

CYR_SORT_KEYS = {c: i for i, c in enumerate(AZBUKA)}


def sort_key(text):
    if not text:
        return [0]
    return [CYR_SORT_KEYS.get(ch, 31) for ch in text]


def cyr_to_lat(text):
    if not text:
        return text
    for c, l in zip(CYRILLIC_CHARS, LATIN_CHARS):
        text = text.replace(c, l)
    text = text.replace('\u0409', 'LJ').replace('\u040A', 'NJ').replace('\u040F', 'D\u017D') \
        .replace('\u0459', 'lj').replace('\u045A', 'nj').replace('\u045F', 'd\u017E') 
    return text


def lat_to_cyr(text):
    if not text:
        return text
    text = text.replace('LJ', '\u0409').replace('Lj', '\u0409').replace('NJ', '\u040A') \
        .replace('Nj', '\u040A').replace('D\u017D', '\u040F').replace('D\u017E', '\u040F') \
        .replace('lj', '\u0459').replace('nj', '\u045A').replace('d\u017e', '\u045F')
    for c, l in zip(CYRILLIC_CHARS, LATIN_CHARS):
        text = text.replace(l, c)
    return text
