"""
Pre-process the given input text.

Pre-processing involves:
1. separating the text into lines according to line delimiters,
2. removing extraneous white spaces,
3. removing punctuation marks, along with various other marks,
"""
import unicodedata


class Splitter:
    _delimiters_names = [
        'ARABIC END OF AYAH', 'ARABIC PLACE OF SAJDAH', 'ARABIC FULL STOP',
        'ARABIC COMMA', 'COMMA', 'TURNED COMMA', 'REVERSED COMMA',
        'ARABIC SEMICOLON', 'SEMICOLON', 'TURNED SEMICOLON', 'REVERSED SEMICOLON'
    ]

    def __init__(self, input_text):
        self._input_text = input_text

    def get_split_lines(self):
        self._split_input_to_lines()
        return self._output_lines

    def _split_input_to_lines(self):
        self._input_text = self._input_text.replace(';', '\n').replace('|', '\n')

        for delimiter in self._delimiters_names:
            self._input_text = self._input_text.replace(unicodedata.lookup(delimiter), '\n')
        self._output_lines = [line for line in self._input_text.splitlines(keepends=False) if line is not '']


class Cleaner:
    _junk_characters = [
        'ARABIC SMALL HIGH TAH', 'ARABIC TRIPLE DOT PUNCTUATION MARK',
        'ARABIC SMALL HIGH LIGATURE SAD WITH LAM WITH ALEF MAKSURA',
        'ARABIC SMALL HIGH LIGATURE QAF WITH LAM WITH ALEF MAKSURA',
        'ARABIC SMALL HIGH MEEM INITIAL FORM', 'ARABIC SMALL HIGH LAM ALEF', 'ARABIC SMALL HIGH JEEM',
        'ARABIC SMALL HIGH THREE DOTS', 'ARABIC SMALL HIGH SEEN', 'ARABIC SMALL HIGH ROUNDED ZERO'
    ]

    def __init__(self, input_lines):
        self._input_lines = []
        for line in input_lines:
            # clean any double white-spaces, splitting to words, then stripping
            self._input_lines.append(' '.join(word.strip() for word in line.split()))

    def get_cleaned_lines(self):
        self._clean_input_lines()
        return self._input_lines

    def _clean_input_lines(self):
        length = len(self._input_lines)
        for junk in self._junk_characters:
            for i in range(length):
                self._input_lines[i] = self._input_lines[i].replace(unicodedata.lookup(junk), '')


def remove_diacritics(text):
    import unicodedata

    def _remove_diacritics(line):
        return ''.join(c for c in unicodedata.normalize('NFC', line) if unicodedata.category(c) != 'Mn')

    if isinstance(text, str):
        return _remove_diacritics(text)
    if isinstance(text, list):
        input_lines_without_diacritics = []
        for s in text:
            input_lines_without_diacritics.append(_remove_diacritics(s))
        return input_lines_without_diacritics


def normalize(text):
    replacement_set = {
        unicodedata.lookup('ARABIC LETTER ALEF WASLA'): unicodedata.lookup('ARABIC LETTER ALEF'),
        unicodedata.lookup('ARABIC LETTER SUPERSCRIPT ALEF'): unicodedata.lookup('ARABIC LETTER ALEF'),
        unicodedata.lookup('ARABIC LETTER ALEF') + unicodedata.lookup('ARABIC SUKUN'): unicodedata.lookup(
            'ARABIC LETTER ALEF'),
        unicodedata.lookup('ARABIC LETTER ALEF WITH MADDA ABOVE'): unicodedata.lookup('ARABIC LETTER ALEF')
    }

    def _normalize_line(line):
        assert isinstance(line, str)
        for key in replacement_set.keys():
            line = line.replace(key, replacement_set.get(key))
        return line

    if isinstance(text, list):
        return [_normalize_line(s) for s in text]
    elif isinstance(text, str):
        return _normalize_line(text)


def preprocess_input(user_input):
    splitter = Splitter(user_input)
    user_input_lines = splitter.get_split_lines()

    cleaner = Cleaner(user_input_lines)
    cleaned_input_lines = cleaner.get_cleaned_lines()

    return cleaned_input_lines
