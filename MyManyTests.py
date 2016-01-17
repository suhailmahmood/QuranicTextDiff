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
    cursor.execute('SELECT verse FROM quran_non_diacritic')
    rows = cursor.fetchall()

    l = []
    for row in rows:
        l.append(row[0])

    input_text = '\n'.join(l)

    splitter = Splitter(input_text)
    split_rows = splitter.get_split_lines()

    cleaner = Cleaner(split_rows)
    cleaned_lines = cleaner.get_cleaned_lines()

    mismatch = 0
    for (row, cl) in zip(rows, cleaned_lines):
        row = row[0].replace('\n', '')
        if row != cl:
            mismatch += 1

    print('No. of mismatch (after running pre-processing on the source in database): {}'.format(mismatch))


def check_verses_in_db_for_newlines():
    import sqlite3

    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    cursor.execute('SELECT verse FROM quran_diacritic')
    rows = cursor.fetchall()

    counter = 0
    verse_count = 0
    for row in rows:
        verse_count += 1
        if row[0].find('\n') > -1:
            counter += 1

    print('No. of newline found: {} in {} verses'.format(counter, verse_count))


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
    import difflib
    for v_nodiac, v_diac_cleaned, surah, verse in zip(verses_non_diacritic, verses_diacritic_cleaned, diac_surah, diac_verse):
        try:
            assert v_nodiac == v_diac_cleaned
        except AssertionError:
            mismatches.append('{}:{}\n{}\n{}\n\n'.format(surah, verse, v_nodiac, v_diac_cleaned))
            # print(mismatches[-1])

    with open('mismatches.txt', 'w', encoding='utf-8') as outfile:
        outfile.write(''.join(mismatches))


if __name__ == '__main__':
    # check_difflib_ratio()
    # see_arabic_chars_unicode()
    # test_pre_processors()
    # check_verses_in_db_for_newlines()
    # arabic_text_diacritic_diff()
    test_remove_diacritic()
