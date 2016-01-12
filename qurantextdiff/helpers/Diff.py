"""

This script is used to compare Quranic texts with/without diacritics, using the python module <code>difflib</code>

The <code>compare()</code> function returns a structure like below:
<code>[
    ( # this is a line, combination of both target line and input line
        [('+ ', 'one'), ('- ', 'two'), ...more words], [('+ ', 'four'), ('- ', 'tow'), ...more words]
    ),
    ( # this is another line
        [('+ ', 'ten'), ('- ', 'nine'), ...more words], [('+ ', 'seven'), ('- ', 'eight'), ...more words]
    ),
    ...
    more lines as tuples
]</code>

 - The function to create html contents creates html with Bootstrap styling.
"""

import difflib

_css_class_diff_added = 'alert-success'
_css_class_diff_deleted = 'alert-danger'
_css_class_diff_changed = 'diff_changed'

_span_tag_template = """<span class="{difftype}">{word}</span>"""

_row_template = """\
    <tr>
        <td>{original_data}</td>
        <td>{input_data}</td>
    </tr>\
"""

_table_template = """\
<table class="table table-striped table-bordered table-hover diff">
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
            pass

    return ' '.join(html_row)


def create_diff_html(tagged_lines):
    rows = []
    for line_pair in tagged_lines:
        original_line_html = _create_html_row(line_pair[0])
        input_line_html = _create_html_row(line_pair[1])
        rows.append(_row_template.format(original_data=original_line_html, input_data=input_line_html))

    return _table_template.format(rows='\n'.join(rows))


def _diff_to_tagged_words(diffs):
    a, b = [], []
    for i, diff in enumerate(diffs):

        if diff.startswith('  '):
            a.append(('  ', diff[2:]))
            b.append(('  ', diff[2:]))

        elif diff.startswith('+ '):
            b.append(('+ ', diff[2:]))

        elif diff.startswith('- '):
            a.append(('- ', diff[2:]))

        elif diff.startswith('? '):
            pass
            # a.append(('? ', diff[2:]))
    return a, b


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


if __name__ == '__main__':
    s1 = ["firstword secondword thirdword", "1stword 2ndward", "onhnred"]
    s2 = ["firstward secendord thirdword", "1stword 2ndrad", "oneundred"]

    # differ = difflib.Differ()
    # result = list(differ.compare([s1[2]], [s2[2]]))
    # import random
    # # random.s
    # s = difflib.SequenceMatcher(None, s1[2], s2[2])
    # print(s.ratio())
    #
    # for r in result:
    #     print(r)
