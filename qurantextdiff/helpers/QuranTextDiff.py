"""
This script is used to compare Quranic texts with/without diacritics, using the python module <code>difflib</code>

1. The <code>compare()</code> function returns a structure as shown below (which is a list of tuples, each tuple being a
line and having two lists, one for original and the other for the input, each list having as many tuples as there are
words in that line, each tuple having two elements, one being a tag from '+ ', '- ', and '? ', and the other the
word itself):
<code>[
    ( # this is a tuple of target line and input line
        [('+ ', 'one'), ('- ', 'two'), ...more words], [('+ ', 'four'), ('- ', 'tow'), ...more words]
    ),
    ( # this is another tuple, the next line comparison
        [('+ ', 'ten'), ('- ', 'nine'), ...more words], [('+ ', 'seven'), ('- ', 'eight'), ...more words]
    ),
    ...
    more tuples each representing a line comparison
]</code>

2. The function to create html contents creates html with <strong>"Bootstrap"</strong> styling.
"""

import difflib

_css_class_diff_added = 'alert-success'
_css_class_diff_deleted = 'alert-danger'
_css_class_diff_changed = 'alert-info'  # change these colors to improve readability

_span_tag_template = """<span class="{difftype}">{word}</span>"""

_row_template = """\
    <tr>
        <td class="id-column">{id}</td>
        <td class="diff diff-column">{original_data}</td>
        <td class="diff diff-column">{input_data}</td>
    </tr>\
"""

_table_template = """\
<table class="table table-striped table-bordered table-hover">
{rows}
</table>\
"""


def compare(original_lines, input_lines):
    """
    <code>original_lines</code>: list(str), list of strings to be compared against, the target.
    <code>input_lines</code>: list(str), list of strings which is compared to s1, the input.
    return: list of tuples containing the each compared strings pair, with each word tagged.
    The returned structure is shown in this scripts docstring
    """
    assert len(original_lines) == len(input_lines)

    tagged_lines = []
    differ = difflib.Differ()

    for original_line, input_line in zip(original_lines, input_lines):
        diff = list(differ.compare(original_line.split(), input_line.split()))
        tagged_lines.append(_diff_to_tagged_words(diff))
    return tagged_lines


def create_diff_html(tagged_lines, identities):
    rows = []
    for line_pair, identity in zip(tagged_lines, identities):
        original_line_html = _create_html_row(line_pair[0])
        input_line_html = _create_html_row(line_pair[1])
        identity_string = '{}:{}'.format(identity[0], identity[1])

        rows.append(_row_template.format(
            id=identity_string,
            original_data=original_line_html,
            input_data=input_line_html)
        )
    return _table_template.format(rows='\n'.join(rows))


def _create_html_row(row_tuples):
    html_row = []
    for elem in row_tuples:
        if elem[0] == "  ":
            html_row.append(elem[1])
        if elem[0] == "+ ":
            html_row.append(_span_tag_template.format(difftype=_css_class_diff_added, word=elem[1]))
        if elem[0] == "- ":
            html_row.append(_span_tag_template.format(difftype=_css_class_diff_deleted, word=elem[1]))
        if elem[0] == "? ":
            html_row.append(_span_tag_template.format(difftype=_css_class_diff_changed, word=elem[1]))

    return ' '.join(html_row)


def _diff_to_tagged_words(diffs):
    original_line, input_line = [], []
    length = len(diffs)

    # need to increment index according to situation, hence not iterating over `diffs`
    # `itertools` could come in handy here, but that can wait for now.
    i = 0
    while i < length:

        if diffs[i].startswith('  '):
            original_line.append(('  ', diffs[i][2:]))
            input_line.append(('  ', diffs[i][2:]))

        elif diffs[i].startswith('+ '):
            input_line.append(('+ ', diffs[i][2:]))

        elif diffs[i].startswith('- '):
            try:
                if diffs[i + 1].startswith('? ') and diffs[i + 2].startswith('+ '):
                    original_line.append(('? ', diffs[i][2:]))
                    input_line.append(('? ', diffs[i + 2][2:]))
                    i += 2
                elif diffs[i + 1].startswith('+ ') and diffs[i + 2].startswith('? '):
                    original_line.append(('? ', diffs[i][2:]))
                    input_line.append(('? ', diffs[i + 1][2:]))
                    i += 2
                else:
                    original_line.append(('- ', diffs[i][2:]))
            except IndexError:
                original_line.append(('- ', diffs[i][2:]))

        elif diffs[i].startswith('? '):
            pass

        i += 1

    return original_line, input_line


def diff_structure_print():
    s1 = ["firstword secondword thirdword", "1stword 2ndward"]
    s2 = ["firstward secendord thirdword", "1stword 2ndrad"]

    result = compare(s1, s2)
    print(result)

    print("\nlevel1")
    for level1 in result:
        print(level1)

    print("\nlevel2")
    for level1 in result:
        for level2 in level1:
            print(level2)

    html_differ = difflib.HtmlDiff()
    html = html_differ.make_file(s1, s2)

    with open('outfile.html', 'w') as outfile:
        outfile.write(html)


if __name__ == '__main__':
    s1 = ['one-hundred', 'one-hunred', 'twothousand', 'one-hundre', 'one-hundred', 'one-hundred']
    s2 = ['one-hundre', 'one-hundrel', 'onhundred', 'one-hundred', 'one-hundrel', 'one-hunrel']

    # differ = difflib.Differ()
    # # for s1elem, s2elem in zip(s1, s2):
    # result = list(differ.compare(s1, s2))
    # for r in result:
    #     print(r)

    result = compare(s1, s2)
    for r in result:
        print(r)
