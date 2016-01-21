from django.db import models


class QuranNonDiacritic(models.Model):
    class Meta:
        db_table = 'quran_non_diacritic'

    surah_no = models.IntegerField()
    verse_no = models.IntegerField()
    verse = models.TextField()


class QuranDiacritic(models.Model):
    class Meta:
        db_table = 'quran_diacritic'

    surah_no = models.IntegerField()
    verse_no = models.IntegerField()
    verse = models.TextField()


class QuranUthmani(models.Model):
    class Meta:
        db_table = 'quran_uthmani'

    surah_no = models.IntegerField()
    verse_no = models.IntegerField()
    verse = models.TextField()
