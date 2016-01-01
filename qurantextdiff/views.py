from django.shortcuts import render


def index_view(request):
    return render(request, 'qurantextdiff/index.html')


# this is rubbish, needs work
def details_view(request):
    surah_no = request.POST.get('surah_no', None)
    verse_start = request.POST.get('verse_start', None)
    # verse_end = request.POST.get('verse_end', None)
    verses = prework.DBQueries.select_verse_range(None, surah_no, verse_start, verse_start)

    mock_inputs = prework.MockInputs.random_mod(verses)

    (original_text, input_text) = prework.StringDiff.compare(verses, mock_inputs)
    contextData = prework.StringDiff.create_diff_html(original_text, input_text)

    return render(request, 'qurantextdiff/details.html', contextData)
