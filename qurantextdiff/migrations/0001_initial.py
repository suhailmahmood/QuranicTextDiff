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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('surah_no', models.IntegerField()),
                ('verse_no', models.IntegerField()),
                ('verse', models.TextField()),
                ('checksum', models.TextField()),
            ],
            options={
                'db_table': 'quran_diacritic',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='QuranNonDiacritic',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('surah_no', models.IntegerField()),
                ('verse_no', models.IntegerField()),
                ('verse', models.TextField()),
                ('checksum', models.TextField()),
            ],
            options={
                'db_table': 'quran_non_diacritic',
                'managed': True,
            },
        ),
    ]
