
def amend_dhalik():
    lines = open('../migrations/0002_required_data_quran_diacritic.txt', encoding='utf-8').readlines()

    pattern = 'ذَلِك'
    replacement = 'ذَٰلِك'

    replacements = 0
    for i, line in enumerate(lines):
        newLine = line
        while newLine.find(pattern) > -1:
            newLine = newLine.replace(pattern, replacement)
            replacements += 1
        lines[i] = newLine

    print('Total {} amendments made'.format(replacements))
    with open('../migrations/0002_required_data_quran_diacritic.txt', 'w', encoding='utf-8') as outfile:
        outfile.write(''.join(lines))


if __name__ == '__main__':
    amend_dhalik()
