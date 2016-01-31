from django.shortcuts import render

from .helpers import MockInputs, QuranicTextDiff, textprocess
from .models import QuranNonDiacritic, QuranDiacritic


def index_view(request):
    return render(request, 'qurantextdiff/index.html')


# this is rubbish, needs work
def details_view(request):
    # Step 1: Preprocessor readies the user input ==> user input is now ready to use for searching
    # Step 2: Search the database to retrieve the identities of the user input
    # Step 3: Send the original text from db and user input and the identities to the differ module
    # Step 4: differ module outputs html, which is ready to render

    user_input1 = request.POST.get('user_input1', None)
    user_input2 = request.POST.get('user_input2', None)
    surah_no = request.POST.get('surah_no', None)
    verse_start = request.POST.get('verse_start', None)
    verse_end = request.POST.get('verse_end', None)

    # only for viewing the Holy Quran
    if not user_input1 and not user_input2:
        query_result = QuranDiacritic.objects.filter(surah_no=surah_no, verse_no__range=(verse_start, verse_end))
        verses = [('{}:{}'.format(q.surah_no, q.verse_no), '{}'.format(q.verse)) for q in query_result]
        return render(request, 'qurantextdiff/details.html', {'qurantable': verses})

    # when input, surah_no and verse_no are given
    if user_input1 and not user_input2:
        preprocessed_input_lines = textprocess.preprocess_input_for_search(user_input1)
        query_result = QuranDiacritic.objects.filter(surah_no=surah_no, verse_no__range=(verse_start, verse_end))
        identities = [(surah_no, v_no) for v_no in range(int(verse_start), int(verse_end) + 1)]

        original_text_lines = [q.verse for q in query_result]
        quranicTextDiff = QuranicTextDiff.QuranicTextDiff(original_text_lines, preprocessed_input_lines)
        original_text_tagged, input_text_tagged = quranicTextDiff.compare()

        html_differ = QuranicTextDiff.HtmlCreator(original_text_tagged, input_text_tagged, identities)
        diff_table = html_differ.create_diff_html()

    # when only two texts are given, nothing more
    if not surah_no and not verse_start and not verse_end:
        preprocessed_input1 = textprocess.preprocess_input_for_search(user_input1)
        preprocessed_input2 = textprocess.preprocess_input_for_search(user_input2)
        original_text_tagged, input_text_tagged = QuranicTextDiff.compare(preprocessed_input1, preprocessed_input2)
        html_differ = QuranicTextDiff.HtmlCreator(original_text_tagged, input_text_tagged, [(0, 0)])
        diff_table = html_differ.create_diff_html()

    return render(request, 'qurantextdiff/details.html', {'difftable': diff_table})
