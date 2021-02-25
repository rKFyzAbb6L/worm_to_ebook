import requests
from bs4 import BeautifulSoup


def get_chapter_html(chapter_url):
    response = requests.get(chapter_url)
    html = response.content
    return html


def get_next_chapter_link(chapter_html):
    soup = BeautifulSoup(chapter_html, 'lxml')
    next_chapter = soup.find('a', text='Next Chapter')
    if next_chapter:
        return next_chapter.get('href')
    else:
        return None


def get_last_chapter_link(chapter_html):
    soup = BeautifulSoup(chapter_html, 'lxml')
    last_chapter = soup.find('a', text='Last Chapter')
    if last_chapter:
        return last_chapter.get('href')
    else:
        return None


def parse_entry_content(html):
    soup = BeautifulSoup(html, 'lxml')
    entry = {'title': soup.find(class_='entry-title').text,
             'content': soup.find('div', 'entry-content')}
    return entry


def parse_chapter(chapter_html):
    nextchapter = get_next_chapter_link(chapter_html)
    prevchapter = get_last_chapter_link(chapter_html)
    entry = parse_entry_content(chapter_html)
    for div in entry['content'].find_all('div', id="jp-post-flair"):
        div.decompose()
    for a in entry['content'].find_all('a'):
        a.decompose()
    entry['content'].smooth()
    chapter_dict = {'chapterTitle': entry['title'],
                    'chapterContent': entry['content'],
                    'nextchapter': nextchapter,
                    'prevchapter': prevchapter}
    return chapter_dict


def get_chapter(chapter_url):
    chapter_html = get_chapter_html(chapter_url)
    chapter = parse_chapter(chapter_html)
    return chapter


def get_book(chapter_url):
    book = {}
    while(True):
        chapter = get_chapter(chapter_url)
        book[chapter_url] = chapter
        chapter_url = chapter['nextchapter']
        if None is chapter_url:
            break
    return book


if __name__ == '__main__':
    book = get_book('https://parahumans.wordpress.com/2013/10/15/speck-30-1/')
    print('')
