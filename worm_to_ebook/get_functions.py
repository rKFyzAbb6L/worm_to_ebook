import requests
import re
from bs4 import BeautifulSoup


def get_chapter_html(chapter_url):
    response = requests.get(chapter_url)
    html = response.content
    return html


def get_sybling_chapter_link(direction, chapter_html):
    # not all chapters match "Next Chapter" perfectly
    # so using a regex search
    soup = BeautifulSoup(chapter_html, 'lxml')
    if direction == 'next':
        sybling_chapter = soup.find('a', string=re.compile('Next Chapter'))
    elif direction == 'prev':
        sybling_chapter = soup.find('a', string=re.compile('Last Chapter'))
    else:
        sybling_chapter = None
    if sybling_chapter:
        return sybling_chapter.get('href')
    else:
        return None


def parse_entry_content(html):
    soup = BeautifulSoup(html, 'lxml')
    entry = {'title': soup.find(class_='entry-title').text,
             'content': soup.find('div', 'entry-content')}
    return entry


def parse_chapter(chapter_url, chapter_html):
    next_chapter = get_sybling_chapter_link('next', chapter_html)
    prev_chapter = get_sybling_chapter_link('prev', chapter_html)
    entry = parse_entry_content(chapter_html)
    for div in entry['content'].find_all('div', id="jp-post-flair"):
        div.decompose()
    for a in entry['content'].find_all('a'):
        a.decompose()
    entry['content'].smooth()
    chapter_dict = {'chapterTitle': str(entry['title']),
                    'chapterUrl': str(chapter_url),
                    'chapterContent': entry['content'].encode(),
                    'nextChapter': str(next_chapter),
                    'prevChapter': str(prev_chapter)}
    return chapter_dict


def get_chapter(chapter_url):
    chapter_html = get_chapter_html(chapter_url)
    chapter = parse_chapter(chapter_url, chapter_html)
    return chapter


def get_book(chapter_url):
    chapter = get_chapter(chapter_url)
    if 'None' == chapter['nextChapter']:
        return [chapter]
    return [chapter] + get_book(chapter['nextChapter'])


if __name__ == "__main__":
    import json
    book = get_book('https://parahumans.wordpress.com' +
                    '/category/stories-arcs-1-10/arc-1-gestation/1-01/')
    with open('worm.json', 'w') as f:
        json.dump({'book': book}, f)
