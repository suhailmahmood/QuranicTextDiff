from django.shortcuts import render

from qurantextdiff.helpers.textprocess import *
from .helpers import QuranicTextDiff
from .models import QuranNonDiacritic, QuranDiacritic


def index_view(request):
    return render(request, 'qurantextdiff/index.html')


def details_view(request):
    user_input = request.POST.get('user_input', None)

    if user_input:
        preprocessed_input_lines = preprocess_input_for_search(user_input)

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
        obj = QuranNonDiacritic.objects.filter(verse__search=line)

        non_diac_verse, sno, vno = obj[0].verse, obj[0].surah_no, obj[0].verse_no
        diac_verse = QuranDiacritic.objects.filter(surah_no=sno, verse_no=vno)[0].verse

        diacritic_verses.append(diac_verse)
        identities.append((obj[0].surah_no, obj[0].verse_no))

    return diacritic_verses, identities
