"""
Pre-process the given input text.

Pre-processing involves:
1. separating the text into lines according to line delimiters,
2. removing extraneous white spaces,
3. removing punctuation marks, along with various other marks,
"""


class Splitter:
    __delimiters_names = [
        'ARABIC END OF AYAH', 'ARABIC PLACE OF SAJDAH', 'ARABIC FULL STOP',
        'ARABIC COMMA', 'COMMA', 'TURNED COMMA', 'REVERSED COMMA',
        'ARABIC SEMICOLON', 'SEMICOLON', 'TURNED SEMICOLON', 'REVERSED SEMICOLON'
    ]

    def __init__(self, input_text):
        self.__input_text = input_text

    def get_split_lines(self):
        self.__split_input_to_lines()
        return self.__output_lines

    def __split_input_to_lines(self):
        self.__input_text = self.__input_text.replace(';', '\n').replace('|', '\n')

        import unicodedata

        for delimiter in self.__delimiters_names:
            self.__input_text = self.__input_text.replace(unicodedata.lookup(delimiter), '\n')
        self.__output_lines = [line for line in self.__input_text.splitlines(keepends=False) if line]


class Cleaner:
    __junk_characters = [
        'ARABIC SMALL HIGH TAH', 'ARABIC TRIPLE DOT PUNCTUATION MARK',
        'ARABIC SMALL HIGH LIGATURE SAD WITH LAM WITH ALEF MAKSURA',
        'ARABIC SMALL HIGH LIGATURE QAF WITH LAM WITH ALEF MAKSURA',
        'ARABIC SMALL HIGH MEEM INITIAL FORM', 'ARABIC SMALL HIGH LAM ALEF', 'ARABIC SMALL HIGH JEEM',
        'ARABIC SMALL HIGH THREE DOTS', 'ARABIC SMALL HIGH SEEN', 'ARABIC SMALL HIGH ROUNDED ZERO',
        # may change later
        'ARABIC MADDAH ABOVE'
    ]

    def __init__(self, input_lines):
        self.__input_lines = []
        for line in input_lines:
            self.__input_lines.append(' '.join(line.split()))

    def get_cleaned_lines(self):
        self.__clean_input_lines()
        return self.__input_lines

    def __clean_input_lines(self):
        length = len(self.__input_lines)
        for junk in self.__junk_characters:
            for i in range(length):
                self.__input_lines[i].replace(junk, '')
