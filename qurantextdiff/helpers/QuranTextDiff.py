"""
This script is used to compare Quranic texts with/without diacritics, using the python module <code>difflib</code>

1. The <code>compare()</code> function returns a structure as shown below (which is a tuple of two lists, each of which
is a nested list, i.e. a list of lists, where each inner list represents a line as a series of tuples, where each tuple
has two elements, the first being the tag and the second the word itself):
<code>
[[('? ', 'firstword1'), ('? ', 'secondword1'), ('  ', 'thirdword1')], [('  ', '1stword1'), ('? ', '2ndword1')]],
[[('? ', 'firstword2'), ('? ', 'secendord2'), ('  ', 'thirdword2')], [('  ', '1stword2'), ('? ', '2ndword2')]]
</code>
The first list shows original text in tagged words form, and the second the input text. In the example each has two
lines.

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


class HtmlCreator:
    def __init__(self, original_lines_tagged, input_lines_tagged, identities):
        self.original_lines_tagged = original_lines_tagged
        self.input_lines_tagged = input_lines_tagged
        self.identities = identities

    def create_diff_html(self):
        rows = []
        for orig_ln_tgd, inp_ln_tgd, identity in zip(self.original_lines_tagged, self.input_lines_tagged,
                                                     self.identities):
            original_line_html = self.__create_html_row(orig_ln_tgd)
            input_line_html = self.__create_html_row(inp_ln_tgd)
            identity_string = '{}:{}'.format(identity[0], identity[1])

            rows.append(_row_template.format(
                id=identity_string,
                original_data=original_line_html,
                input_data=input_line_html)
            )
        return _table_template.format(rows='\n'.join(rows))

    def __create_html_row(self, tagged_line):
        """
        Creates html for a single row in any of the two data columns (original or input)
        """
        html_row = []
        for tagged_word in tagged_line:
            # each "tagged_word" is a tuple: (tag, word)
            if tagged_word[0] == "  ":
                html_row.append(tagged_word[1])
            if tagged_word[0] == "+ ":
                html_row.append(_span_tag_template.format(difftype=_css_class_diff_added, word=tagged_word[1]))
            if tagged_word[0] == "- ":
                html_row.append(_span_tag_template.format(difftype=_css_class_diff_deleted, word=tagged_word[1]))
            if tagged_word[0] == "? ":
                html_row.append(_span_tag_template.format(difftype=_css_class_diff_changed, word=tagged_word[1]))

        return ' '.join(html_row)


def compare(original_lines, input_lines):
    """
    <code>original_lines</code>: list(str), list of strings to be compared against, the target.
    <code>input_lines</code>: list(str), list of strings which is compared to s1, the input.
    return: list of tuples containing the each compared strings pair, with each word tagged.
    The returned structure is shown in this scripts docstring
    """
    assert len(original_lines) == len(input_lines)

    differ = difflib.Differ()
    original_lines_tagged, input_lines_tagged = [], []

    for original_line, input_line in zip(original_lines, input_lines):
        diff = list(differ.compare(original_line.split(), input_line.split()))
        olt, ilt = _diff_to_tagged_words(diff)
        original_lines_tagged.append(olt)
        input_lines_tagged.append(ilt)
    return original_lines_tagged, input_lines_tagged


def _diff_to_tagged_words(diffs):
    original_line_tagged, input_line_tagged = [], []
    length = len(diffs)

    # need to increment index according to situation, hence not iterating over `diffs`
    # `itertools` could come in handy here, but that can wait for now.
    i = 0
    while i < length:
        # '  ' means word in diffs[i] is same in both the lines
        if diffs[i].startswith('  '):
            original_line_tagged.append(('  ', diffs[i][2:]))
            input_line_tagged.append(('  ', diffs[i][2:]))
        # '+ ' means word in diffs[i] is an added word in the input line
        elif diffs[i].startswith('+ '):
            input_line_tagged.append(('+ ', diffs[i][2:]))
        # '- ' means word in diffs[i] is deleted from the original line
        # if diffs[i+1] or diffs[i+2] doesn't have '? ' tag, the word is "deleted" from the original line
        # if however diffs[i+1] or diffs[i+2] has '? ' tag, the word is "changed"
        elif diffs[i].startswith('- '):
            try:
                if diffs[i + 1].startswith('? ') and diffs[i + 2].startswith('+ '):
                    original_line_tagged.append(('? ', diffs[i][2:]))
                    input_line_tagged.append(('? ', diffs[i + 2][2:]))
                    i += 2
                elif diffs[i + 1].startswith('+ ') and diffs[i + 2].startswith('? '):
                    original_line_tagged.append(('? ', diffs[i][2:]))
                    input_line_tagged.append(('? ', diffs[i + 1][2:]))
                    i += 2
                else:
                    original_line_tagged.append(('- ', diffs[i][2:]))
            except IndexError:
                original_line_tagged.append(('- ', diffs[i][2:]))
        # this part is handled in the above elif branch
        elif diffs[i].startswith('? '):
            pass

        i += 1

    return original_line_tagged, input_line_tagged


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

    # html_differ = difflib.HtmlDiff()
    # html = html_differ.make_file(s1, s2)
    #
    # with open('outfile.html', 'w') as outfile:
    #     outfile.write(html)


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
