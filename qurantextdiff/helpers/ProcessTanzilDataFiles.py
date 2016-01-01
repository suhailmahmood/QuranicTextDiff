
file_names = [
    'quran-simple-clean.txt',
    'quran-simple.txt'
]


def process_tanzil_files(old_contents) -> list:
    """
    Pre-processes a tanzil.net file of plain Quranic texts so that each surah begins with the surah number on a line
    and the beginning of each surah does not have the 'Bismillah', as is there in the original files. Requires the data
    files to be in this directory and named as given in the list `file_names`.
    :rtype: list of lines of texts to be written to a file as having pre-processed texts
    :param old_contents: list containing the contents of tanzil.net file of plain Quranic texts
    """

    Bismilla = old_contents[0].replace('\n', '') + ' '
    surah_tauba_marker = 1235
    surah_counter = 1
    new_contents = ['#1\n']

    for i, line in enumerate(old_contents):
        verse = line.replace('\n', '')

        if line.startswith(Bismilla) or i == surah_tauba_marker:
            surah_counter += 1
            verse = line.replace(Bismilla, '')
            verse = verse.replace('\n', '')
            new_contents.append('\n#{}\n'.format(surah_counter))
        new_contents.append(verse + '\n')

    return new_contents


if __name__ == '__main__':

    for file_name in file_names:
        new_file_name = 'new_' + file_name

        print("opening file {}...".format(file_name))
        old_file = open(file_name, 'r', encoding='utf-8')
        new_file = open(new_file_name, 'w', encoding='utf-8')
        new_contents = process_tanzil_files(old_file.readlines())

        print("writing to file {}...".format(new_file_name))
        new_file.writelines(new_contents)
