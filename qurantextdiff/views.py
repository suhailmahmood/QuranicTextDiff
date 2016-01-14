from django.shortcuts import render

from .helpers import MockInputs, QuranTextDiff, Preprocess
from .models import QuranNonDiacritic


def index_view(request):
    return render(request, 'qurantextdiff/index.html')


# this is rubbish, needs work
def details_view(request):
    surah_no = request.POST.get('surah_no', None)
    verse_start = request.POST.get('verse_start', None)
    verse_end = request.POST.get('verse_end', None)

    query_result = QuranNonDiacritic.objects.filter(surah_no=surah_no, verse_no__range=(verse_start, verse_end))

    original_text = [q.verse for q in query_result]
    input_text = MockInputs.create_mock_inputs(original_text)

    preprocessed_input = Preprocess.preprocess_input(input_text)

    identities = [(surah_no, v_no) for v_no in range(int(verse_start), int(verse_end)+1)]

    results = QuranTextDiff.compare(original_text, input_text)
    diff_table = QuranTextDiff.create_diff_html(results, identities)

    return render(request, 'qurantextdiff/details.html', {'difftable': diff_table})
