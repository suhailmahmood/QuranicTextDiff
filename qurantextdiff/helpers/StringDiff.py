import difflib
from http.client import NOT_IMPLEMENTED


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


def tag_words(diffs):
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
            if diffs[i-1].startswith(''):
                pass
    print_func_output(tag_words, s1=a, s2=b)
    return a, b


def compare(s1, s2):
    """
    :param s1: the string to be compared against, the target string
    :param s2: the string which is compared to s1, the input string
    :rtype: tuple containing the two compared strings, with each word tagged
    """
    s1 = s1.split()
    s2 = s2.split()
    d = difflib.Differ()
    result = list(d.compare(s1, s2))
    (s12, s22) = tag_words(result)
    return s12, s22


def create_diff_html(original_text, input_text):
    raise NOT_IMPLEMENTED
    pass


def cache_generator(gen):
    if isinstance(gen, (list, tuple, dict)):
        return gen
    else:
        return list(gen)


def main():
    # s1 = "one  thre twoo one"
    # s2 = "one towo tree"
    s1 = "two three nine eleven"
    s2 = "one four five six seven two three elevan"

    s11, s22 = compare(s1, s2)

    print(s1)
    print(s2)
    print(s11)
    print(s22)




if __name__ == '__main__':
    main()
