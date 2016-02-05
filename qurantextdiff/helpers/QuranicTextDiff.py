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
import unicodedata

import qurantextdiff.helpers.textprocess as textprocess


class HtmlCreator:
    _css_class_diff_added = 'alert-success'
    _css_class_diff_deleted = 'alert-danger'
    _css_class_diff_changed = 'alert-info'  # change these colors to improve readability

    _span_tag_template = '<span class="{difftype}">{word}</span>'
    _span_tag_template_tooltip = '<span class="{difftype}" data-toggle="tooltip" data-placement="bottom" \
title="{tooltip}">{word}</span>'

    _row_template = """\
    <tr>
        <td class="id-column">{id}</td>
        <td class="arabic">{original_data}</td>
        <td class="arabic">{input_data}</td>
    </tr>\
"""

    _table_template = """\
<table class="table table-striped table-bordered table-hover">
{rows}
</table>
"""

    def __init__(self, original_lines_tagged, input_lines_tagged, identities):
        self.original_lines_tagged = original_lines_tagged
        self.input_lines_tagged = input_lines_tagged
        self.identities = identities

    def create_diff_html(self):
        rows = []
        for orig_ln_tgd, inp_ln_tgd, identity in zip(self.original_lines_tagged, self.input_lines_tagged,
                                                     self.identities):
            original_line_html = self._create_html_row(orig_ln_tgd)
            input_line_html = self._create_html_row(inp_ln_tgd)
            identity_string = '{}:{}'.format(identity[0], identity[1])

            rows.append(self._row_template.format(
                id=identity_string,
                original_data=original_line_html,
                input_data=input_line_html)
            )
        return self._table_template.format(rows='\n'.join(rows))

    def _create_html_row(self, tagged_line):
        """
        Creates html for a single row in any of the two data columns (original or input)
        """
        html_row = []

        for t in tagged_line:
            # each 't' is a tuple: (tag, word [, word_pair])
            # when tag is '? ', word_pair is present for input line, in all other cases it is not passed

            tag, content = t[0], t[1]
            has_tooltip = True if len(t) == 3 else False
            if tag == "  ":
                html_row.append(content)
            if tag == "+ ":
                html_row.append(
                    self._span_tag_template.format(difftype=self._css_class_diff_added, word=content))
            if tag == "- ":
                html_row.append(
                    self._span_tag_template.format(difftype=self._css_class_diff_deleted, word=content))
            if tag == "? ":
                if has_tooltip:
                    html_row.append(
                        self._span_tag_template_tooltip.format(difftype=self._css_class_diff_changed, word=content,
                                                               tooltip=self._create_tooltip(t[2][0], t[2][1])))
                else:
                    html_row.append(
                        self._span_tag_template.format(difftype=self._css_class_diff_changed, word=content))
        return ' '.join(html_row)

    def _create_tooltip(self, s1, s2):
        # still using normalisation on the original text. With enough modification of the original text,
        # this won't be necessary
        # inp_word in already normalised
        tooltip = []
        inserts, deletes, replaces, displacements = [], [], [], []

        sm = difflib.SequenceMatcher(None, textprocess.normalize(s1), s2)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == 'insert':
                inserts.append([s2[j1:j2], i1, False])
            elif tag == 'delete':
                deletes.append([s1[i1:i2], i1, False])
            elif tag == 'replace':
                replaces.append([s1[i1:i2], s2[j1:j2], i1])

        for d in deletes:
            for i in inserts:
                if d[0] == i[0] and d[2] is False and i[2] is False:
                    displacements.append((d[0], d[1], i[1]))
                    d[2] = True
                    i[2] = True
                    break

        for chrs, f, t in displacements:
            tooltip.append('Displaced {} from {} to {}'.format(chrs, f + 1, t + 1))
        for d in deletes:
            if d[2] is False:
                tooltip.append('Deleted {} at {}'.format(d[0], d[1]))
        for i in inserts:
            if i[2] is False:
                tooltip.append('Inserted {} at {}'.format(i[0], i[1]))
        for r in replaces:
            tooltip.append('Replaced {} with {} at {}'.format(r[0], r[1], r[2]))

        return '\n'.join(tooltip)


class QuranicTextDiff:
    def __init__(self, original_lines, input_lines):
        assert len(original_lines) == len(input_lines)
        self.original_lines = original_lines
        self.input_lines = input_lines
        self.input_lines_normalized = textprocess.normalize(input_lines)

    def compare(self):
        original_lines_tagged, input_lines_tagged = [], []

        for lineNo, (origLn, inpLnNormalised) in enumerate(zip(self.original_lines, self.input_lines_normalized)):
            olt, ilt = self._diff_to_tagged_words(origLn, inpLnNormalised, lineNo)
            original_lines_tagged.append(olt)
            input_lines_tagged.append(ilt)
        return original_lines_tagged, input_lines_tagged

    def _diff_to_tagged_words(self, original_line, input_line_normalised, line_no):
        differ = difflib.Differ()
        original_line_tagged, input_line_tagged = [], []

        original_words = original_line.split()
        input_words = self.input_lines[line_no].split()
        input_words_normalised = input_line_normalised.split()

        diffs = list(differ.compare(original_words, input_words_normalised))
        length = len(diffs)
        orig_index, inp_index = 0, 0

        i = 0
        while i < length:
            if diffs[i].startswith('  '):
                original_line_tagged.append(('  ', original_words[orig_index]))
                input_line_tagged.append(('  ', input_words[inp_index]))
                orig_index += 1
                inp_index += 1

            # CASE: a word not present in original line is 'added' to the input line
            elif diffs[i].startswith('+ '):
                input_line_tagged.append(('+ ', input_words[inp_index]))
                inp_index += 1
            elif diffs[i].startswith('- '):
                orig_word = diffs[i][2:]
                try:
                    if diffs[i + 1].startswith('? '):  # then diffs[i+2] starts with ('+ '), obviously
                        inp_word_norm = diffs[i + 2][2:]
                        changed = self._is_change_significant(orig_word, inp_word_norm)
                        tag = '? ' if changed else '  '

                        original_line_tagged.append((tag, original_words[orig_index]))
                        input_line_tagged.append(
                            (tag, input_words[inp_index],
                             (orig_word, inp_word_norm) if changed else input_words[inp_index]))

                        i += 3 if i + 3 < length and diffs[i + 3].startswith('? ') else 2
                        orig_index += 1
                        inp_index += 1

                    # checking i+2<length before diffs[i+2].startswith.. ==> to enable short-circuit
                    elif diffs[i + 1].startswith('+ ') and i + 2 < length and diffs[i + 2].startswith('? '):
                        inp_word_norm = diffs[i + 1][2:]
                        changed = self._is_change_significant(orig_word, inp_word_norm)

                        tag = '? ' if changed else '  '

                        original_line_tagged.append((tag, original_words[orig_index]))
                        input_line_tagged.append(
                            (tag, input_words[inp_index],
                             (orig_word, inp_word_norm) if changed else input_words[inp_index]))

                        i += 2
                        orig_index += 1
                        inp_index += 1

                    # CASE: which difflib considers as 'deletion' and 'addition', rather than as 'change'
                    # as in the first two branches.
                    # checking i+1<length before diffs[i+1].startswith.. ==> to enable short-circuit
                    elif i + 1 < length and diffs[i + 1].startswith('+ '):
                        inp_word_norm = diffs[i + 1][2:]
                        changed = self._is_change_significant(diffs[i][2:], inp_word_norm)
                        tag = '? ' if changed else '  '

                        original_line_tagged.append((tag, original_words[orig_index]))
                        input_line_tagged.append(
                            (tag, input_words[inp_index],
                             (orig_word, inp_word_norm) if changed else input_words[inp_index]))

                        i += 1
                        orig_index += 1
                        inp_index += 1

                    # CASE: a word deleted from the original line
                    else:
                        original_line_tagged.append(('- ', original_words[orig_index]))
                        orig_index += 1
                except IndexError:
                    pass
            i += 1
        return original_line_tagged, input_line_tagged

    def _is_change_significant(self, original_text, input_text):
        # still using normalization on the original text. With enough modification of the original text,
        # this won't be necessary
        original_text_normalised = textprocess.normalize(original_text)
        input_text_normalised = textprocess.normalize(input_text)

        differ = difflib.Differ()
        diffs = list(differ.compare([original_text_normalised], [input_text_normalised]))

        guide_lines = [diff[2:] for diff in diffs if diff.startswith('? ')]

        changed = False
        for guide_line in guide_lines:
            for i, c in enumerate(guide_line):
                # unicodedata.category(c)) is wrong
                if c == '+' or c == '?' or (c == '-' and unicodedata.category(c)) != 'Mn':
                    changed = True

        if changed:
            printDebug('Returning True for:')
            printDebug('{}\n{}'.format(original_text_normalised, input_text_normalised))
            return True

        printDebug('Returning False for:')
        printDebug('{}\n{}'.format(original_text_normalised, input_text_normalised))
        return False


def printDebug(s):
    debug = False
    if debug:
        print(s)
