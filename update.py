import urllib.request
import xml.etree.ElementTree as ET
import json
import contextlib
import shutil
import datetime
import os.path
import os
import sys

url = 'https://www.youtube.com/feeds/videos.xml?playlist_id=PLRJNAhZxtqH_3Nl-7n1vhgTUHyFSuQ0nI'
datefmt = '%Y-%m-%dT%H:%M:%S+00:00'
destroot = "wwwroot"

CHEATING = set([
    "Treasury Secretary Mnuchin Briefs Reporters",
    "Press Briefing with Acting Director of US Citizenship and Immigration Services Ken Cuccinelli",
    "Press Briefing with Acting Commissioner of Customs and Border Protection Mark Morgan",
    "Press Briefing with Secretary Pompeo and Secretary Mnuchin",
])

ns = {
    'atom': 'http://www.w3.org/2005/Atom',
    'media': 'http://search.yahoo.com/mrss/',
    'yt': 'http://www.youtube.com/xml/schemas/2015',
}

def get_latest():
    with urllib.request.urlopen(url) as f:
        data = ET.fromstring(f.read().decode('utf-8'))

    infos = []
    for entry in data.findall('atom:entry', ns):
        datestr = entry.find('atom:published', ns).text
        date = datetime.datetime.strptime(datestr, datefmt)
        date = date.replace(tzinfo=datetime.timezone.utc)
        info = {
            'date': date,
            'title': entry.find('atom:title', ns).text,
            'url': entry.find('atom:link', ns).attrib['href'],
        }
        if info['title'] in CHEATING:
            continue
        infos.append(info)

    infos.sort(key=lambda d: d['date'], reverse=True)
    info = infos[0]
    return info

def move(src):
    _, head = os.path.split(src)
    truedest = os.path.join(destroot, head)
    try:
        dest_mtime = os.stat(truedest).st_mtime
    except FileNotFoundError:
        dest_mtime = 0
    if os.stat(src).st_mtime - dest_mtime > 0:
        print(src, '->', truedest)
        shutil.copy2(src, destroot)

@contextlib.contextmanager
def generate(name):
    truedest = os.path.join(destroot, name)
    print('generating', truedest)
    try:
        yield open(truedest + '.tmp', 'w')
    finally:
        shutil.move(truedest + '.tmp', truedest)

def main():
    # make sure we are working where we think we are
    base, _ = os.path.split(os.path.abspath(__file__))
    os.chdir(base)

    fetch = not '-n' in sys.argv

    if fetch:
        print('fetching rss...')
        info = get_latest()
        local = info['date'].astimezone()
        print('last conference was', local.strftime("%a %b %d, %H:%M %Z"))

    move("src/index.html")
    move("src/icon.png")
    move("src/preview.png")
    move("src/pressbriefing.js")
    move("src/pressbriefing.css")
    move("extern/jquery-3.4.0.min.js")
    move("extern/flipclock/compiled/flipclock.min.js")
    move("extern/flipclock/compiled/flipclock.css")

    if fetch:
        info['date'] = info['date'].strftime(datefmt)
        with generate('start.js') as f:
            f.write('var startInfo = {};\n'.format(json.dumps(info)))
        with generate('update.json') as f:
            f.write('{}\n'.format(json.dumps(info)))

if __name__ == "__main__":
    main()
