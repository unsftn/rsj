import re
import pdfplumber


PAGE_NUMBER_AT_END = re.compile(r'[0-9]+$')


def nop(page_text):
    return page_text


def clean_fixed_content(page_text, content):
    if not page_text:
        return page_text
    return page_text.replace(content+'\n', '').replace(content, '')


def clean_hyphens_at_end_of_line(page_text):
    if not page_text:
        return page_text
    return page_text.replace('-\n', '').replace('- \n', '')


def clean_page_number_at_end_of_page(page_text):
    if not page_text:
        return page_text
    return re.sub(PAGE_NUMBER_AT_END, '', page_text)


def merge_lines_ending_with_blank(page_text):
    if not page_text:
        return page_text
    return page_text.replace(' \n', ' ')


def clean_page(page_text, operations):
    for o in operations:
        operation = OPERATION_DEFINITIONS.get(o['opcode'], OPERATION_DEFINITIONS[0]).get('function')
        if not operation:
            continue
        params = o['params']
        if params:
            page_text = operation(page_text, *params)
        else:
            page_text = operation(page_text)
    return page_text.strip()


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


def init_tags(page_text):
    paras = page_text.split('\n')
    tagged_paras = []
    for para in paras:
        words = para.split()
        tagged_words = ' '.join([f'<span class="word word{index} untagged">{word}</span>' for index, word in enumerate(words) if word])
        tagged_paras.append(tagged_words)
    return '\n'.join(tagged_paras)


OPERATION_DEFINITIONS = {
    0: {'description': 'do nothing', 'function': nop, 'params': []},
    1: {'description': 'clean fixed content', 'function': clean_fixed_content, 'params': ['content']},
    2: {'description': 'clean hyphens at end of line', 'function': clean_hyphens_at_end_of_line, 'params': []},
    3: {'description': 'clean page number at end of page', 'function': clean_page_number_at_end_of_page, 'params': []},
    4: {'description': 'merge lines ending with blank', 'function': merge_lines_ending_with_blank, 'params': []},
}
