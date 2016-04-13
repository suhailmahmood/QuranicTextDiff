import difflib

from django.shortcuts import render

from qurantextdiff.helpers.textprocess import *
from .helpers import QuranicTextDiff, urlprocess
from .models import QuranNonDiacritic, QuranDiacritic


def index_view(request):
    return render(request, 'qurantextdiff/index.html')


def details_view(request):
    user_input = request.POST.get('user_input', None)
    user_url = request.POST.get('user_url', None)

    if user_input:
        preprocessed_input_lines = preprocess_input(user_input)

        original_text_lines, identities = search(preprocessed_input_lines)
        quranicTextDiff = QuranicTextDiff.QuranicTextDiff(original_text_lines, preprocessed_input_lines)
        original_text_tagged, input_text_tagged = quranicTextDiff.compare()

        html_differ = QuranicTextDiff.HtmlCreator(original_text_tagged, input_text_tagged, identities)
        diff_table = html_differ.create_diff_html()
    elif user_url:
        candidate_verses = get_candidate_verses(user_url)
        preprocessed_input_lines = preprocess_input(candidate_verses)

        original_text_lines, identities = search(preprocessed_input_lines)
        quranicTextDiff = QuranicTextDiff.QuranicTextDiff(original_text_lines, preprocessed_input_lines)
        original_text_tagged, input_text_tagged = quranicTextDiff.compare()

        html_differ = QuranicTextDiff.HtmlCreator(original_text_tagged, input_text_tagged, identities)
        diff_table = html_differ.create_diff_html()

    return render(request, 'qurantextdiff/details.html', {'difftable': diff_table})


def search(input_lines):
    searchable = remove_diacritics(normalize(input_lines))

    diacritic_verses, identities = [], []
    for line in searchable:
        rows = QuranNonDiacritic.objects.filter(verse__search=line)

        row = highest_match_row(rows, line)

        sno, vno = row.surah_no, row.verse_no
        diac_verse = QuranDiacritic.objects.filter(surah_no=sno, verse_no=vno)[0].verse

        diacritic_verses.append(diac_verse)
        identities.append((row.surah_no, row.verse_no))

    return diacritic_verses, identities


def get_candidate_verses(fromURL):
    candidate_verses = []
    arabic_texts = urlprocess.urldata(fromURL)

    # print('Collecting candidate verses...', end=' ')
    for i, line in enumerate(arabic_texts):
        cleaned_line = remove_diacritics(normalize(line))
        rows = QuranNonDiacritic.objects.filter(verse__search=cleaned_line)
        if rows:
            orig_verse = highest_match_row(rows, cleaned_line).verse
            sm = difflib.SequenceMatcher(None, orig_verse, cleaned_line)
            ratio = sm.ratio()
            if ratio >= 0.5:
                candidate_verses.append(line)

    # print('Done')
    return candidate_verses


def highest_match_row(rows, line):
    ratio, idx = 0, 0
    for i, row in enumerate(rows):
        sm = difflib.SequenceMatcher(None, row.verse, line)
        if sm.ratio() > ratio:
            ratio = sm.ratio()
            idx = i

    return rows[idx]
