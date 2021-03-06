# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QuranDiacritic',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('surah_no', models.IntegerField()),
                ('verse_no', models.IntegerField()),
                ('verse', models.TextField()),
            ],
            options={
                'db_table': 'quran_diacritic',
            },
        ),
        migrations.CreateModel(
            name='QuranNonDiacritic',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('surah_no', models.IntegerField()),
                ('verse_no', models.IntegerField()),
                ('verse', models.TextField()),
            ],
            options={
                'db_table': 'quran_non_diacritic',
            },
        ),
        migrations.CreateModel(
            name='QuranUthmani',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('surah_no', models.IntegerField()),
                ('verse_no', models.IntegerField()),
                ('verse', models.TextField()),
            ],
            options={
                'db_table': 'quran_uthmani',
            },
        ),
    ]
