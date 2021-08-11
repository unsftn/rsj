import unicodedata


def remove_punctuation(text):
    cleared_text = ''.join(c for c in text if unicodedata.category(c) in ['Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'NI', 'Zs'])
    return cleared_text
