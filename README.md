# QuranTextDiff

Various forums/blogs quote many Quranic verses, and in doing so some unintentional mistakes might crop up, or even worse
could happen when someone tries to tamper the Quranic texts by forgery. What this web application does (or better *will
do* when it is complete!) is check Quranic quotes in any web page for its correctness by comparing against an authentic
version in the backend.

This is my project for my Undergraduate final year. I am doing this in django, and principal workhorse of this application
is python's [difflib](http://docs.python.org/3.5/library/difflib.html#module-difflib) library.

Suggestions/advices are highly solicited!

## Setting up MySQL database

 - Create a database:
	named 'qurandb',
	user 'qurandbuser',
	password 'mypass'
 - Run `py manage.py makemigrations` and `py manage.py migrate` commands
 - Then create full-text index for the column `verse` in the table `quran_non_diacritic`.

Refer to these links if need be:
 - Setting up FT search in MySQL: stackoverflow.com/questions/2248743/django-mysql-full-text-search
 - Problem: "No migrations to apply": stackoverflow.com/questions/33086444/django-1-8-migrate-is-not-creating-tables

---

Setting up elasticsearch (version used 2.2.0):

 - Download elasticsearch (zip file)
 - Extract to any suitable location
 - Go to elasticsearch-x.x.x\bin in cmd
 - Type service, and hit enter.
 - Follow the instructions


Setting up Haystack (version used 2.4.1):

 - Either download using `pip install django-haystack`, or
 - go to https://pypi.python.org/pypi/django-haystack and download the version you want
