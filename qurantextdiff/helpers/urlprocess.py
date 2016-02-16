import re
from bs4 import BeautifulSoup
import urllib.request
import guess_language


def urldata(url):
    print('...in urldata()')
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()

    soup = BeautifulSoup(html, 'html.parser')
    print('...soup created')
    text_findAll = soup.findAll(text=True)
    print('...findAll completed...')

    visible_texts = []
    for line in filter(visible, text_findAll):
        line = line.strip()
        if line:
            visible_texts.append(line)
    print('...filtering completed')
    arabic = []
    for l in visible_texts:
        if guess_language.guess_language(l) == 'ar':
            arabic.append(l)

    print('...returning urldata')
    return arabic


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True

if __name__ == '__main__':
    ar = urldata('http://www.altafsir.com/Tafasir.asp?tMadhNo=2&tTafsirNo=73&tSoraNo=4&tAyahNo=24&tDisplay=yes&UserProfile=0&LanguageId=2')
    print('Printing from urlprocess')
    for a in ar:
        print(a)
    print('Done ... Printing from urlprocess')
