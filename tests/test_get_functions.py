import pytest
import requests

from worm_to_ebook import __version__
from worm_to_ebook.get_functions import (get_book,
                                         get_chapter_html,
                                         get_sybling_chapter_link,
                                         parse_entry_content,
                                         parse_chapter,
                                         get_chapter)
from bs4 import BeautifulSoup


def test_version():
    assert __version__ == '0.1.0'


BAD_HTML = b'<body><a href=https://fake.test>FakeLink<a></body>'

GOOD_HTML = b'''
<body>
<a href=https://next.test>Next Chapter</a>
<a href=https://prev.test>Last Chapter</a>
<div class=entry-title>Arc 47</div>
<div class=entry-content>
a giant story. </br>
with unsane html formatting <p>
thanks wordpress
</div>
</body>
'''


def get_soup():
    bad_soup = BeautifulSoup(BAD_HTML, 'lxml')
    good_soup = BeautifulSoup(GOOD_HTML, 'lxml')
    return (bad_soup, good_soup)


class MockResponse():
    content = BAD_HTML


def mock_get(*args, **kwargs):
    return MockResponse()


def test_get_chapter_html(monkeypatch):
    monkeypatch.setattr(requests, 'get', mock_get)
    result = get_chapter_html('https://fake.fake')
    assert BAD_HTML == result


def test_get_next_chapter_link():
    bad_soup, good_soup = get_soup()
    bad_result = get_sybling_chapter_link('next', BAD_HTML)
    good_result = get_sybling_chapter_link('next', GOOD_HTML)
    assert bad_result == None
    assert good_result == good_soup.find('a', text='Next Chapter').get('href')


def test_get_prev_chapter_link():
    bad_soup, good_soup = get_soup()
    bad_result = get_sybling_chapter_link('prev', BAD_HTML)
    good_result = get_sybling_chapter_link('prev', GOOD_HTML)
    assert bad_result == None
    assert good_result == good_soup.find('a', text='Last Chapter').get('href')


def test_parse_entry_content():
    bad_soup, good_soup = get_soup()
    expected = {
        'title': 'Arc 47',
        'content': good_soup.find('div', 'entry-content')
    }
    good_result = parse_entry_content(GOOD_HTML)
    assert expected == good_result
    with pytest.raises(AttributeError):
        parse_entry_content(BAD_HTML)


def test_parse_chapter():
    bad_soup, good_soup = get_soup()
    expected = {
        'chapterTitle': 'Arc 47',
        'chapterUrl': 'http://fake.test',
        'chapterContent': good_soup.find('div', 'entry-content').encode(),
        'nextChapter': 'https://next.test',
        'prevChapter': 'https://prev.test'
    }
    result = parse_chapter('http://fake.test', GOOD_HTML)
    assert expected == result


def test_get_chapter(monkeypatch):
    bad_soup, good_soup = get_soup()
    expected = {
        'chapterTitle': 'Arc 47',
        'chapterUrl': 'http://fake.test',
        'chapterContent': good_soup.find('div', 'entry-content').encode(),
        'nextChapter': 'https://next.test',
        'prevChapter': 'https://prev.test'
    }
    monkeypatch.setattr(
        'worm_to_ebook.get_functions.get_chapter_html', lambda x: GOOD_HTML)
    result = get_chapter('http://fake.test')
    assert expected == result


def mock_get_chapter(chapter_url):
    if chapter_url == 'http://fake.test':
        return {
            'chapterTitle': 'Arc 47',
            'chapterUrl': 'http://fake.test',
            'chapterContent': 'fake',
            'nextChapter': 'https://next.test',
            'prevChapter': 'https://prev.test'
        }
    return {
        'chapterTitle': 'Arc 48',
        'chapterUrl': 'http://fake.test',
        'chapterContent': 'fake',
        'nextChapter': 'None',
        'prevChapter': 'https://prev.test'
    }


def test_get_book(monkeypatch):

    expected = [{
        'chapterTitle': 'Arc 47',
        'chapterUrl': 'http://fake.test',
        'chapterContent': 'fake',
        'nextChapter': 'https://next.test',
        'prevChapter': 'https://prev.test'
        },
        {
        'chapterTitle': 'Arc 48',
        'chapterUrl': 'http://fake.test',
        'chapterContent': 'fake',
        'nextChapter': 'None',
        'prevChapter': 'https://prev.test'
    }]
    monkeypatch.setattr(
        'worm_to_ebook.get_functions.get_chapter', mock_get_chapter)
    result = get_book('http://fake.test')
    assert expected == result
