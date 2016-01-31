from tkinter.ttk import *


def check_difflib_ratio():
    """
    Finds the minimum value of SequenceMatcher.ratio() for two strings such that Differ considers them as 'changed'.
    """
    import difflib
    import random
    import string

    def random_modify_string(input_string, change_word=0.5, change_char=0.3):
        word_list = input_string.split()
        for i, word in enumerate(word_list):
            if random.random() < change_word:
                for j in range(len(word)):
                    if random.random() < change_char:
                        word = word[:j] + random.choice(string.printable) + word[j + 1:]

                word_list[i] = word

        return ' '.join(word_list)

    differ = difflib.Differ()
    min_ratio = 1.0

    for count in range(1000):
        length = random.randint(5, 100)
        s1 = ''.join(random.SystemRandom().choice(string.printable) for _ in range(length))
        s2 = random_modify_string(s1)

        sm = difflib.SequenceMatcher(None, s1, s2)
        ratio = sm.ratio()
        result = list(differ.compare([s1], [s2]))

        for line in result:
            if line.startswith('?'):
                if ratio < min_ratio:
                    min_ratio = ratio
                    break

    print('Minimum ratio which difflib considers as "change" is: {}'.format(min_ratio))


def see_arabic_chars_unicode():
    """
    Arabic character set ranges from 0600–06FF in unicode.
    """
    import unicodedata
    absent = 0
    present = 0
    for i in range(0x0600, 0x06FF + 1):
        try:
            print('{:04X} \t{} --> {}'.format(i, unicodedata.name(chr(i)), chr(i)))
            present += 1
        except ValueError:
            absent += 1
    else:
        print('\nTotal present: {}'.format(present))
        print('\nTotal absent: {}'.format(absent))


def test_pre_processors():
    import sqlite3
    from qurantextdiff.helpers.textprocess import Cleaner, Splitter

    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    cursor.execute('SELECT verse FROM quran_diacritic')
    rows = [row[0] for row in cursor.fetchall()]

    input_text = '\n'.join(rows)

    splitter = Splitter(input_text)
    split_rows = splitter.get_split_lines()

    cleaner = Cleaner(split_rows)
    cleaned_lines = cleaner.get_cleaned_lines()

    mismatch = 0
    for (row, cl) in zip(rows, cleaned_lines):
        if row != cl:
            mismatch += 1

    print('No. of mismatch (after running pre-processing on the source in database): {}'.format(mismatch))


def test_remove_diacritic():
    import sqlite3
    from qurantextdiff.helpers import textprocess

    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()

    cursor.execute('SELECT * FROM quran_non_diacritic')
    quran_non_diacritic_rows = cursor.fetchall()

    cursor.execute('SELECT * FROM quran_diacritic')
    quran_diacritic_rows = cursor.fetchall()

    verses_diacritic = [row[3] for row in quran_diacritic_rows]
    diac_surah = [row[1] for row in quran_diacritic_rows]
    diac_verse = [row[2] for row in quran_diacritic_rows]
    verses_non_diacritic = [row[3] for row in quran_non_diacritic_rows]

    verses_diacritic_cleaned = textprocess.remove_diacritics(verses_diacritic)

    mismatches = []
    for v_nodiac, v_diac_cleaned, surah, verse in zip(verses_non_diacritic, verses_diacritic_cleaned, diac_surah,
                                                      diac_verse):
        try:
            assert v_nodiac == v_diac_cleaned
        except AssertionError:
            mismatches.append('{}:{}\n{}\n{}\n\n'.format(surah, verse, v_nodiac, v_diac_cleaned))
            print(mismatches[-1])

    with open('mismatches.txt', 'w', encoding='utf-8') as outfile:
        outfile.write(''.join(mismatches))

    print('Testing: "{}()"'.format(test_remove_diacritic.__name__))
    print('Comparing non-diacritic verses with diacritic ones with their\ndiacritics removed'
          ' using "remove_diacritic()" function...')
    print('No. of mismatch lines found: {}'.format(len(mismatches)))


def test_diff_result_diacritic():
    import difflib

    with open('sample_input.txt', 'r', encoding='utf-8') as input_file:
        inputs = input_file.readlines()
    s1 = [inputs[0].replace('\n', '')]
    s2 = [inputs[1].replace('\n', '')]
    differ = difflib.Differ()
    diffs = list(differ.compare(s1, s2))

    for diff in diffs:
        print(diff)
    import unicodedata
    for i in range(len(diffs)):
        if diffs[i].startswith('? '):
            guide_word = diffs[i][2:]
            word = diffs[i-1][2:]
            for index in range(len(guide_word)):
                guide = guide_word[index]
                if guide == '-' or guide == '^' or guide == '+':
                    # print('{} {}'.format(guide, index))
                    print(unicodedata.name(word[index]))


def check_presence_of_patterns():
    import unicodedata as ud
    import sqlite3

    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM quran_diacritic')
    rows = cursor.fetchall()

    ALIF = ud.lookup('ARABIC LETTER ALEF')
    SUKUN = ud.lookup('ARABIC SUKUN')
    WASLA = ud.lookup('ARABIC LETTER ALEF WASLA')
    ALIF_SUPER = ud.lookup('ARABIC LETTER SUPERSCRIPT ALEF')
    ALIF_MADDA = ud.lookup('ARABIC LETTER ALEF WITH MADDA ABOVE')
    MEEM = ud.lookup('ARABIC LETTER MEEM')
    SHADDA = ud.lookup('ARABIC SHADDA')
    NOON = ud.lookup('ARABIC LETTER NOON')
    HAMZA = ud.lookup('ARABIC LETTER HAMZA')
    DAMMA = ud.lookup('ARABIC DAMMA')
    WAW = ud.lookup('ARABIC LETTER WAW')
    KASRA = ud.lookup('ARABIC KASRA')
    KASRATAN = ud.lookup('ARABIC KASRATAN')
    FATHA = ud.lookup('ARABIC FATHA')

    # pattern = MEEM + SUKUN + ud.lookup('SPACE') + MEEM
    # pattern = ALIF_MADDA + HAMZA
    pattern = DAMMA + WAW + ALIF


    # pattern = 'هُوَ'
    pattern_count = 0
    empty_sukun_count = 0
    outfile = open('presence-count.txt', 'w', encoding='utf-8')
    for row in rows:
        index = row[3].find(pattern)
        if index > -1:
            pattern_count += 1
            if row[3][index+1] != SUKUN:
                empty_sukun_count += 1
                print('{}:{}'.format(row[1], row[2]), file=outfile)
                print(row[3], file=outfile)

    print('Pattern count: {}'.format(pattern_count))
    print('Empty sukun count: {}'.format(empty_sukun_count))


def test_IndexError():
    l = [i+1 for i in range(5)]
    copy = []
    for i in range(10):
        try:
            copy.append(l[i])
            if i == 1:
                copy.append(l[i][0])
        except Exception:
            pass
        print(copy)


def test_normalize_function():
    import sqlite3
    from difflib import Differ, SequenceMatcher
    import qurantextdiff.helpers.textprocess as textprocess

    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM quran_diacritic')
    diacritic_verses = []
    surah_no = []
    verse_no = []
    for row in cursor.fetchall():
        surah_no.append(row[1])
        verse_no.append(row[2])
        diacritic_verses.append(row[3])

    cursor.execute('SELECT * FROM quran_non_diacritic')
    non_diacritic_verses = [row[3] for row in cursor.fetchall()]

    diacritic_verses_normalized = textprocess.normalize(textprocess.remove_diacritics(diacritic_verses))

    mismatches = []
    mismatch_chars = []

    for s_no, v_no, diac, ndiac in zip(surah_no, verse_no, diacritic_verses_normalized, non_diacritic_verses):
        try:
            assert diac == ndiac
        except AssertionError:
            for c1, c2 in zip(diac, ndiac):
                if c1 != c2:
                    if c1 not in mismatch_chars:
                        mismatch_chars.append(c1)
                    if c2 not in mismatch_chars:
                        mismatch_chars.append(c2)

            mismatches.append((s_no, v_no, diac, ndiac))

    file = open('mismatches.txt', 'w', encoding='utf-8')
    for s, v, d, n in mismatches:
        print('{}:{}\n{}\n{}\n'.format(s, v, d, n), file=file)

    print(len(mismatch_chars))
    print('\n'.join(mismatch_chars))


def check_presence_of_dhalik():
    import sqlite3
    # pattern_d = 'ذَلِك'
    # pattern_d = 'ذَٰلِك'
    pattern_d = 'ذَالِك'
    pattern_n = 'ذلك'

    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM quran_diacritic')
    diacritic_verses = []
    s_no_d = []
    v_no_d = []
    for row in cursor.fetchall():
        s_no_d.append(row[1])
        v_no_d.append(row[2])
        diacritic_verses.append(row[3])

    cursor.execute('SELECT * FROM quran_non_diacritic')
    non_diacritic_verses = []
    s_no_n = []
    v_no_n = []
    for row in cursor.fetchall():
        s_no_n.append(row[1])
        v_no_n.append(row[2])
        non_diacritic_verses.append(row[3])

    counter = 0
    for s_d, s_n, v_d, v_n, verse_d, verse_n in zip(s_no_d, s_no_n, v_no_d, v_no_n, diacritic_verses, non_diacritic_verses):
        verse_d = str(verse_d)
        if verse_d.find(pattern_d) > -1:
            try:
                assert verse_n.find(pattern_n) > -1
                assert s_d == s_n
                assert v_d == v_n
                counter += 1
            except AssertionError:
                assert s_d == s_n
                assert v_d == v_n
                print('{}:{}\n{}\n{}'.format(s_d, v_d, verse_d, verse_n))
    print(counter)


if __name__ == '__main__':
    check_presence_of_dhalik()
