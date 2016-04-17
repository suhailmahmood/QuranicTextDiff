import binascii
import difflib

from django.shortcuts import render

from qurantextdiff.helpers.textprocess import *
from .helpers import QuranicTextDiff, urlprocess
from .models import QuranNonDiacritic, QuranDiacritic

orig_checksum = None
changed_checksum = None


def index_view(request):
    return render(request, 'qurantextdiff/index.html')


def details_view(request):
    user_input = request.POST.get('user_input', None)
    user_url = request.POST.get('user_url', None)

    if user_input:
        candidate_verses = user_input
    elif user_url:
        candidate_verses = get_candidate_verses(user_url)

    if user_input or user_url:
        preprocessed_input_lines = preprocess_input(candidate_verses)
        original_text_lines, identities = search(preprocessed_input_lines)
        quranicTextDiff = QuranicTextDiff.QuranicTextDiff(original_text_lines, preprocessed_input_lines)
        original_text_tagged, input_text_tagged = quranicTextDiff.compare()

        html_differ = QuranicTextDiff.HtmlCreator(original_text_tagged, input_text_tagged, identities)
        diff_table = html_differ.create_diff_html()

        return render(request, 'qurantextdiff/details.html', {'difftable': diff_table})
    else:
        return render(request, 'qurantextdiff/index.html')


def ft(request):
    print('check in POST:', 'check' in request.POST)
    print('finject in POST:', 'finject' in request.POST)

    if 'check' not in request.POST and 'finject' not in request.POST:
        return render(request, 'qurantextdiff/ft.html', {'display_chosen_verse': 'none', 'display_results': 'none'})

    elif 'check' in request.POST and 'finject' not in request.POST:
        print("'check' in request.POST and 'finject' not in request.POST")
        s_no = request.POST.get('surah_no', None)
        v_no = request.POST.get('verse_no', None)
        type = request.POST.get('type', None)
        print(s_no, v_no, type)

        global orig_checksum
        if type == 'diacritic':
            chosen_verse = QuranDiacritic.objects.filter(surah_no=s_no, verse_no=v_no)[0].verse
            orig_checksum = QuranDiacritic.objects.filter(surah_no=s_no, verse_no=v_no)[0].orig_verse_crc
        else:
            chosen_verse = QuranNonDiacritic.objects.filter(surah_no=s_no, verse_no=v_no)[0].verse
            orig_checksum = QuranNonDiacritic.objects.filter(surah_no=s_no, verse_no=v_no)[0].orig_verse_crc
        return render(request, 'qurantextdiff/ft.html',
                      {'chosen_verse': chosen_verse, 'display_chosen_verse': 'body', 'display_results': 'none'})

    elif 'finject' in request.POST:
        global orig_checksum, changed_checksum
        changed_checksum = binascii.crc32(request.POST.get('verse_area').encode())
        return render(request, 'qurantextdiff/ft.html',
                      {'display_chosen_verse': 'body', 'display_results': 'body', 'orig_checksum': orig_checksum,
                       'changed_checksum': changed_checksum})


def search(input_lines):
    searchable = remove_diacritics(normalize(input_lines))

    diacritic_verses, identities = [], []
    for i, line in enumerate(searchable):
        rows = QuranNonDiacritic.objects.filter(verse__search=line)

        row = highest_match_row(rows, line)

        sno, vno = row.surah_no, row.verse_no
        diac_row_obj = QuranDiacritic.objects.filter(surah_no=sno, verse_no=vno)[0]

        check_crc(diac_row_obj)

        diac_row_obj.input_verse = input_lines[i]
        diac_row_obj.input_verse_crc = binascii.crc32(input_lines[i].encode())
        diac_row_obj.save()

        diacritic_verses.append(diac_row_obj.verse)
        identities.append((row.surah_no, row.verse_no))

    return diacritic_verses, identities


def get_candidate_verses(fromURL):
    candidate_verses = []
    arabic_texts = urlprocess.urldata(fromURL)

    for i, line in enumerate(arabic_texts):
        cleaned_line = remove_diacritics(normalize(line))
        rows = QuranNonDiacritic.objects.filter(verse__search=cleaned_line)
        if rows:
            orig_verse = highest_match_row(rows, cleaned_line).verse
            sm = difflib.SequenceMatcher(None, orig_verse, cleaned_line)
            ratio = sm.ratio()
            if ratio >= 0.5:
                candidate_verses.append(line)
                QuranNonDiacritic.objects.filter()

    return candidate_verses


def highest_match_row(rows, line):
    ratio, idx = 0, 0
    for i, row in enumerate(rows):
        sm = difflib.SequenceMatcher(None, row.verse, line)
        if sm.ratio() > ratio:
            ratio = sm.ratio()
            idx = i

    return rows[idx]


def check_crc(row_obj):
    new_crc = binascii.crc32(row_obj.verse.encode())
    # try:
    assert row_obj.orig_verse_crc == new_crc
    # except AssertionError:
    #     print('Assertion Failed: crc mismatch for surah_no: {}, verse_no: {}'.format(row_obj.surah_no,
    #                                                                                       row_obj.verse_no))
    #     print('CRCs:\nOriginal crc: {}\nNew crc: {}'.format(row_obj.orig_verse_crc, new_crc))
