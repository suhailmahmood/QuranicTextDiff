# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def read_data_file_content(file_selector):
    """
    Reads the *required_data* file, chosen by `file_selector` and returns the contents
    :param file_selector: 0 for diacritic version and 1 for non-diacritic one
    :return: list containing the contents of the file, each *line* as an element of list
    """
    files = [
        r'qurantextdiff\\migrations\\0002_required_data_quran_diacritic.txt',
        r'qurantextdiff\\migrations\\0002_required_data_quran_non_diacritic.txt'
    ]
    contents = open(files[file_selector], 'r', encoding='utf-8').readlines()
    return contents


def load_initial_data(apps, schema_editor):
    """
    Populates the Models `QuranDiacritic` and `QuranNonDiacritic`, using data from the method `read_data_file_content()`
    """

    QuranDiacriticModel = apps.get_model('qurantextdiff', 'QuranDiacritic')
    QuranNonDiacriticModel = apps.get_model('qurantextdiff', 'QuranNonDiacritic')

    AppModels = [QuranDiacriticModel, QuranNonDiacriticModel]

    for selector, AppModel in enumerate(AppModels):
        lines = read_data_file_content(selector)
        surah_counter = 0
        verse_counter = 1
        objs = []

        for i, line in enumerate(lines):
            if line == '\n':
                continue
            if line.startswith('#'):
                surah_counter += 1
                verse_counter = 1
                continue
            else:
                objs.append(AppModel(surah_no=surah_counter, verse_no=verse_counter, verse=line))
                verse_counter += 1

        AppModel.objects.bulk_create(objs)


class Migration(migrations.Migration):

    dependencies = [
        ('qurantextdiff', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_data)
    ]
