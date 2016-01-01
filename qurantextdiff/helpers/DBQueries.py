import sqlite3


def select_verse_range(table, surah_no, verse_start, verse_end):
    if table is None:
        table = 'quran_simple_clean'

    conn = sqlite3.connect('temp.db')
    dbcursor = conn.cursor()
    select_command = "SELECT verse FROM {} WHERE surah_no=? AND verse_no>=? AND verse_no<=?".format(table)
    parameters = [surah_no, verse_start, verse_end]
    dbcursor.execute(select_command, parameters)
    verses = [verse[0] for verse in dbcursor.fetchall()]

    return verses

if __name__ == "__main__":
    rows = select_verse_range(None, 1, 1, 7)
    for i, v in enumerate(rows):
        print("{} :{}".format(v, i + 1))
