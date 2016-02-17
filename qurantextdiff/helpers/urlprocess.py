import re
from bs4 import BeautifulSoup
import urllib.request
import guess_language


def urldata(url):
    print('Opening page...', end=' ')
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    print('Done')

    print('Parsing...', end=' ')
    soup = BeautifulSoup(html, 'html.parser')
    print('Done')
    # print(soup.prettify())

    print('Finding all text...', end=' ')
    text_findAll = soup.findAll(text=True)
    print('Done')

    print('Filtering visible texts...', end=' ')
    visible_texts = []
    for line in filter(visible, text_findAll):
        line = line.strip()
        if line:
            visible_texts.append(line)
    print('Done')

    print('Filtering arabic texts...', end=' ')
    arabic = []
    for l in visible_texts:
        if guess_language.guess_language(l) == 'ar':
            arabic.append(l)
    print('Done')
    return arabic


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True
