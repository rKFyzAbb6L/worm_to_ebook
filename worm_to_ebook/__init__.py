__version__ = '0.1.0'

from urllib import request
from bs4 import BeautifulSoup
from ebooklib import epub
import re

# i hope this doesn't change. I don't think it has for a while.
CONTENTS = 'https://parahumans.wordpress.com/table-of-contents/'


# gethtml   _DONE
# getshittywordpresscontents   _DONE
# parseshittywordpressedhtml   _mostly DONE
# makeepubcontents
# makeepubchapter

def get_worm_html(url):
    '''
    take a url, and return its html
    '''
    with request.urlopen(url) as response:
        html = response.read()
    return html


def not_contents(href):
    notcontents = re.compile(r"table-of-contents")
    return href and not notcontents.search(href)


def get_arc_chapter_url(arcTitle):
    '''
    get all the chapter URLs for a given a bs4 navigable string Arc's Title 
    '''

    arcChapterUrls = [x.get('href') for x in arcTitle.parent.find_all('a')]
    return (str(arcTitle), arcChapterUrls)

def get_entry_content(html):
    soup = BeautifulSoup(html, 'lxml')
    entrycontent = soup.find('div', 'entry-content')
    return entrycontent

def parse_worm_contents(contentsHtml):
    '''
    take html from contents and return a list of dicts with
    key of arc and child items of chapter URLs

    all chapters at in 1.01 or 1.x format, except epilogue and sequel teaser
    '''
    # actually should get the Arc title as well,
    # then maybe just use tha tas the key to a dict with value list of chapters

    # get main contents
    contents = get_entry_content(contentsHtml)

    # Arc title regex. _usually_ <p><strong>Arc <\br>

    # so now.... Find arc title, find all chapterUrls until next Arc title.
    # i don't think they're actualy child tags, just mostly sort of sequential,
    # but not actually necessarilly in proper order

    # i might be able to find the arc title. use next_element until i get first
    # <a href>, save that link, then continue harvesting until I don't match
    # then finally "reset" to next index from chapter title match, and repeat

    # list of Arc titles, with cleanup for inconsistent tagging
    for strong in contents.find_all('strong'):
        strong.unwrap()

    contents.smooth()

    arcTitles = contents.find_all(string=re.compile(r'Arc \d+:.+'))
    chapterUrls = list(map(get_arc_chapter_url, arcTitles))

    return chapterUrls


def parse_worm_chapter(chapterHtml):
    '''
    take html from worm chapter, and turn just the story portion
    '''
    # story seems to be in <p> tags wrapped in <div class="entry-content">
    # except where it's not
    storyParent = get_entry_content(chapterHtml)
    # destructive, but get rid of extra tags that hopefully aren't arc titles
    for div in storyParent.find_all('div', id="jp-post-flair"):
        div.decompose()
    for a in storyParent.find_all('a'):
        a.decompose()
    storyParent.smooth()
    return storyParent


def make_you_epub():
    '''
    epub is html, so just mash it up in there?
    '''
    pass
    # chapters = [worm.parse_worm_chapter(worm.get_worm_html(url)) for url in contents[:5]]
    # for chapter in chapters:
    #     c1.content=u'<h1>arc 30</h1>' + str(chapter)
#get next link. basically give start chapter and start crawling through.
#BeautifulSoup(worm.get_worm_html(contents[0]),'lxml').find('a',text='Next Chapter')['href']
