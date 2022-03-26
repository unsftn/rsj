import re
import string
import pdfplumber


PAGE_NUMBER_AT_END = re.compile(r'[0-9]+$')
PAGE_NUMBER_AT_TOP = re.compile(r'^[0-9]+')


def nop(page_text):
    return page_text


def clean_fixed_content(page_text, page_number, content):
    if not page_text:
        return page_text
    content = content.replace('\u2e31', ' ')
    return page_text.replace(content+'\n', '').replace(content, '')


def clean_hyphens_at_end_of_line(page_text, page_number):
    if not page_text:
        return page_text
    return page_text.replace('-\n', '').replace('- \n', '')


def clean_page_number_at_end(page_text, page_number):
    if not page_text:
        return page_text
    return re.sub(PAGE_NUMBER_AT_END, '', page_text)


def clean_page_number_at_top(page_text, page_number):
    if not page_text:
        return page_text
    return re.sub(PAGE_NUMBER_AT_TOP, '', page_text)


def merge_lines_ending_with_blank(page_text, page_number):
    if not page_text:
        return page_text
    return page_text.replace(' \n', ' ')


def remove_starting_pages(page_text, page_number, numberofpages):
    if page_number <= int(numberofpages):
        return ''
    else:
        return page_text


def clean_page(page_text, operations):
    for o in operations:
        operation = FILTER_LOOKUP.get(o['opcode'], FILTER_LOOKUP[0]).get('function')
        if not operation:
            continue
        params = o['params']
        kwargs = {p['name']: p['value'] for p in params}
        page_text = operation(page_text, **kwargs)
        # if params:
        #     page_text = operation(page_text, **kwargs)
        # else:
        #     page_text = operation(page_text)
    return page_text.strip()


def extract_pdf_file(file_name):
    pages = []
    with pdfplumber.open(file_name) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if not page_text:
                continue
            pages.append(page_text)
    return pages


def clean_pdf_file(file_name, operations):
    pages = []
    with pdfplumber.open(file_name) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if not page_text:
                continue
            page_text = clean_page(page_text, operations)
            if not page_text:
                continue
            pages.append(page_text)
    return pages


# def filter_publication(pub_id):
#     try:
#         publikacija = Publikacija.objects.get(id=pub_id)
#
#     except Publikacija.DoesNotExist:
#         return None


def default_status(word):
    if word == '—':
        return 'ignore'
    return 'ignore' if all(ch.isdigit() or ch in string.punctuation for ch in word) else 'untagged'


def init_tags(page_text):
    paras = page_text.split('\n')
    tagged_paras = []
    for para in paras:
        words = para.split()
        tagged_words = ' '.join([f'<span class="word w{index} {default_status(word)}">{word}</span>' for index, word in enumerate(words) if word])
        tagged_paras.append(tagged_words)
    return '\n'.join(tagged_paras)


FILTERS = [
    {'code': 0, 'description': 'Ништа', 'function': nop, 'page': True,
     'params': []},
    {'code': 1, 'description': 'Уклони фиксан садржај', 'function': clean_fixed_content, 'page': True,
     'params': [{'name': 'content', 'title': 'Текст', 'value': ''}]},
    {'code': 2, 'description': 'Уклони хифенацију', 'function': clean_hyphens_at_end_of_line, 'page': True,
     'params': []},
    {'code': 3, 'description': 'Уклони број странице на дну', 'function': clean_page_number_at_end, 'page': True,
     'params': []},
    {'code': 4, 'description': 'Уклони број странице на врху', 'function': clean_page_number_at_top, 'page': True,
     'params': []},
    {'code': 5, 'description': 'Спој линије које се завршавају размаком', 'function': merge_lines_ending_with_blank,
     'params': [], 'page': True},
    {'code': 6, 'description': 'Уклони почетне странице', 'function': remove_starting_pages, 'page': False,
     'params': [{'name': 'numberofpages', 'title': 'Број страница', 'value': ''}]}
]

FILTER_CHOICES = [(x['code'], x['description']) for x in FILTERS]

FILTER_LOOKUP = {x['code']: x for x in FILTERS}

DOCUMENT_FILTERS = [f for f in FILTERS if not f['page']]

PAGE_FILTERS = [f for f in FILTERS if f['page']]


def get_filter(code):
    return FILTER_LOOKUP.get(code, None)


def invoke_filter(filter_code, params, page_text, page_number):
    fil = get_filter(filter_code)
    kwargs = {p['name']: p['value'] for p in params}
    return fil['function'](page_text, page_number, **kwargs)


def get_filter_list():
    return [{'code': f['code'], 'description': f['description'], 'params': f['params']} for f in FILTERS if f['code'] != 0]
