# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib

from django.db import migrations


def read_data_file_content(file_selector):
    files = [
        r'qurantextdiff\migrations\0002_required_data_quran_diacritic.txt',
        r'qurantextdiff\migrations\0002_required_data_quran_non_diacritic.txt'
    ]
    contents = open(files[file_selector], 'r', encoding='utf-8').readlines()
    return contents


def load_initial_data(apps, schema_editor):
    quran_diacritic_model = apps.get_model('qurantextdiff', 'QuranDiacritic')
    quran_non_diacritic_model = apps.get_model('qurantextdiff', 'QuranNonDiacritic')

    models = [quran_diacritic_model, quran_non_diacritic_model]

    for selector, model in enumerate(models):
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
                verse = line.replace('\n', '')
                checksum = hashlib.md5(verse.encode('utf-8')).hexdigest()
                objs.append(model(surah_no=surah_counter, verse_no=verse_counter, verse=verse, checksum=checksum))
                verse_counter += 1

        model.objects.bulk_create(objs)


class Migration(migrations.Migration):
    dependencies = [
        ('qurantextdiff', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_data)
    ]
