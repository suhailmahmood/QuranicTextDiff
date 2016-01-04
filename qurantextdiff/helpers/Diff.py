import difflib

_table_template = """\
<table class="diff">
    {rows}
</table>"""

_row_template = """\
<tr>
        <td>{data}</td>
    </tr>"""


def compare(s1, s2):
    """
    :param s1: list of strings to be compared against, the target
    :param s2: list of strings which is compared to s1, the input
    :rtype: list of tuples containing the each compared strings pair, with each word tagged
    """
    assert len(s1) == len(s2)

    tagged_lines = []
    d = difflib.Differ()

    for orig, inp in zip(s1, s2):
        diff = list(d.compare(orig, inp))
        tagged_lines.append(_tag_words(diff))

    return tagged_lines


def create_diff_html():
    pass


def _tag_words(diffs):
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
            if diffs[i - 1].startswith(''):
                pass
    # print_func_output(tag_words, s1=a, s2=b)
    return a, b


def print_raw_diff(diffs):
    print("In function: ----------- {} -----------".format(print_func_output.__name__))
    for diff in diffs:
        if diff.endswith('\n'):
            print(diff, end='')
        else:
            print(diff)


def print_func_output(function, **kwargs):
    print("In function: ----------- {} -----------".format(function.__name__))
    for arg in kwargs:
        arg_type = type(kwargs[arg])
        if arg_type is list:
            print("{}:\t{}".format(arg, kwargs[arg]))
        elif arg_type is dict:
            print(arg)
            for e in kwargs[arg]:
                print("\t{}: {}".format(e, kwargs[arg][e]))
    print()


def describe_diff(diffs):
    desc = {'added': [], 'deleted': [], 'changed': [], 'unchanged': []}
    for i, diff in enumerate(diffs):
        if diff.startswith('- '):
            desc['deleted'].append(diff[2:])
        elif diff.startswith('+ '):
            desc['added'].append(diff[2:])
        elif diff.startswith('? '):
            desc['changed'].append(diff[2:])
        elif diff.startswith('  '):
            desc['unchanged'].append(diff[2:])

    print_func_output(describe_diff, description=desc)
    return desc


def main():
    # s1 = "one  thre twoo one"
    # s2 = "one towo tree"
    s1 = ["one three five nine eleven", "one three five nine eleven", "one three five nine eleven"]
    s2 = ["one four five  nine elevan", "one four five  nine elevan", "one four five  nine elevan"]

    # s11, s22 = compare(s1, s2)


if __name__ == '__main__':
    main()
