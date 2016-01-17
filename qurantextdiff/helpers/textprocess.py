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
            self._input_lines.append(' '.join(line.split()))

    def get_cleaned_lines(self):
        self._clean_input_lines()
        return self._input_lines

    def _clean_input_lines(self):
        length = len(self._input_lines)
        for junk in self._junk_characters:
            for i in range(length):
                self._input_lines[i].replace(unicodedata.lookup(junk), '')


def preprocess_input(user_input):
    splitter = Splitter(user_input)
    user_input_lines = splitter.get_split_lines()

    cleaner = Cleaner(user_input_lines)
    cleaned_input_lines = cleaner.get_cleaned_lines()

    return cleaned_input_lines


def remove_diacritics(input_lines):
    import unicodedata

    non_diacritic_lines = []
    for line in input_lines:
        non_diacritic_lines.append(''.join(c for c in unicodedata.normalize('NFD', line)
                                           if unicodedata.category(c) != 'Mn'))
    return non_diacritic_lines
