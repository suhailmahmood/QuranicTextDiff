import re
from bs4 import BeautifulSoup
import urllib.request


def urldata(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()

    soup = BeautifulSoup(html, 'html.parser')
    text_findAll = soup.findAll(text=True)

    visible_texts = []
    for line in filter(visible, text_findAll):
        line = line.strip()
        if line:
            visible_texts.append(line)

    arabic = []
    for l in visible_texts:
        if is_arabic(l):
            arabic.append(l)
    return arabic


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    elif re.match('\n', str(element)):
        return False
    return True


def is_arabic(s):
    if any(0x0600 <= ord(c) <= 0x06ff for c in s):
        return True
    return False
