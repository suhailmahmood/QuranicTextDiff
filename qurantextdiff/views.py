from django.shortcuts import render

from .models import QuranNonDiacritic
from .helpers import MockInputs, Diff


def index_view(request):
    return render(request, 'qurantextdiff/index.html')


# this is rubbish, needs work
def details_view(request):
    surah_no = request.POST.get('surah_no', None)
    verse_start = request.POST.get('verse_start', None)
    verse_end = request.POST.get('verse_end', None)

    query_result = QuranNonDiacritic.objects.filter(surah_no=surah_no, verse_no__range=(verse_start, verse_end))

    original_text = [q.verse for q in query_result]
    mock_inputs = MockInputs.create_mock_inputs(original_text)

    results = Diff.compare(original_text, mock_inputs)
    diff_table = Diff.create_diff_html(results)

    return render(request, 'qurantextdiff/details.html', {'difftable': diff_table})
