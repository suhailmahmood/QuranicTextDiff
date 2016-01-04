from django.shortcuts import render

from .models import QuranNonDiacritic
from .helpers import MockInputs


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

    diffs = []
    for i, orig in enumerate(original_text):
        diff_tuple = original_text[i], mock_inputs[i]
        diffs.append(diff_tuple)

    return render(request, 'qurantextdiff/details.html', {'diffs': diffs})

