from django.shortcuts import render

from .helpers import MockInputs, QuranTextDiff, textprocess
from .models import QuranNonDiacritic, QuranDiacritic


def index_view(request):
    return render(request, 'qurantextdiff/index.html')


# this is rubbish, needs work
def details_view(request):
    # Step 1: Preprocessor readies the user input ==> user input is now ready to use for searching
    # Step 2: Search the database to retrieve the identities of the user input
    # Step 3: Send the original text from db and user input and the identities to the differ module
    # Step 4: differ module outputs html, which is ready to render

    user_input = request.POST.get('user_input', None)
    surah_no = request.POST.get('surah_no', None)
    verse_start = request.POST.get('verse_start', None)
    verse_end = request.POST.get('verse_end', None)

    if not user_input:
        query_result = QuranNonDiacritic.objects.filter(surah_no=surah_no, verse_no__range=(verse_start, verse_end))

        original_text = [q.verse for q in query_result]
        input_text = MockInputs.create_mock_inputs(original_text)

        # preprocessed_input = Preprocess.preprocess_input(input_text)

        identities = [(surah_no, v_no) for v_no in range(int(verse_start), int(verse_end) + 1)]

        original_text_tagged, input_text_tagged = QuranTextDiff.compare(original_text, input_text)
        html_differ = QuranTextDiff.HtmlCreator(original_text_tagged, input_text_tagged, identities)
        diff_table = html_differ.create_diff_html()
    else:
        preprocessed_input = textprocess.preprocess_input(user_input)
        query_result = QuranDiacritic.objects.filter(surah_no=surah_no, verse_no__range=(verse_start, verse_end))
        identities = [(surah_no, v_no) for v_no in range(int(verse_start), int(verse_end) + 1)]

        original_text = [q.verse for q in query_result]
        original_text_tagged, input_text_tagged = QuranTextDiff.compare(original_text, preprocessed_input)
        html_differ = QuranTextDiff.HtmlCreator(original_text_tagged, input_text_tagged, identities)
        diff_table = html_differ.create_diff_html()

    return render(request, 'qurantextdiff/details.html', {'difftable': diff_table})
