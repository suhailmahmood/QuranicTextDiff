def random_mod_string(input_string, change_word=0.8, change_char=0.3):
    import random, string

    word_list = input_string.split()

    # selecting any word at random for modification within the word
    for i, word in enumerate(word_list):
        if random.random() < change_word:
            # selecting any index within the word at random,
            # and modifying it with a random character in [0x0627, 0x0645]
            for j in range(len(word)):
                if random.random() < change_char:
                    word = word[:j] + random.choice(string.ascii_letters+string.digits) + word[j + 1:]

            word_list[i] = word

    return ' '.join(word_list)


def check_difflib_ratio():
    import string, random, difflib

    differ = difflib.Differ()
    min_ratio = 1.0

    for count in range(1000):
        length = random.randint(5, 100)
        s1 = ''.join(random.SystemRandom().choice(string.printable) for _ in range(length))
        s2 = random_mod_string(s1)

        sm = difflib.SequenceMatcher(None, s1, s2)
        ratio = sm.ratio()
        result = list(differ.compare([s1], [s2]))

        for line in result:
            if line.startswith('?'):
                if ratio < min_ratio:
                    min_ratio = ratio
                    break

    print('Minimum ratio which difflib considers as "change" is: {}'.format(min_ratio))


if __name__ == '__main__':
    check_difflib_ratio()
