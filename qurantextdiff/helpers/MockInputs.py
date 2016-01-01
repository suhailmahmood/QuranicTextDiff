import random


def create_mock_inputs(original, delete_word=0.1, misplace_word=0.1, change_word=0.3, change_char=0.3):
    """
    Creates mock inputs by modifying the strings passed in `original`. A certain modification is carried out when a
    random number generated is less than or equal to the probability set for that particular change.
    :param original: list of strings. Each item of the list is a sentence.
    :param delete_word: probability for deleting a word from the original string
    :param misplace_word: probability for displacing a word within the original string
    :param change_word: probability for selecting a word for modifying its characters
    :param change_char: probability for changing a character of a word chosen for modification
    :return: list containing the modified sentences, maintaining the original positions as in the original list
    """
    mock_input = []

    for index, line in enumerate(original):
        word_list = line.split()

        # removing any word at random
        for word in word_list:
            if random.random() <= delete_word:
                word_list.remove(word)

        # displacing any word at random
        for i in range(len(word_list)):
            if random.random() <= misplace_word:
                word = word_list.pop(i)
                new_loc = random.randrange(0, len(word_list))
                word_list.insert(new_loc, word)

        # selecting any word at random for modification within the word
        for i, word in enumerate(word_list):
            if random.random() <= change_word:
                # selecting any index within the word at random,
                # and modifying it with a random character in [0x0627, 0x0645]
                for j in range(len(word)):
                    if random.random() < change_char:
                        word = word[:j] + chr(random.randrange(0x0627, 0x0645)) + word[j + 1:]

                word_list[i] = word

        mock_input.append(' '.join(word_list))

    return mock_input
