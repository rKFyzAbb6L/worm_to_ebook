__version__ = '0.1.0'

from urllib import request
from bs4 import BeautifulSoup
import re

# i hope this doesn't change. I don't think it has for a while.
CONTENTS = 'https://parahumans.wordpress.com/table-of-contents/'

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

def parse_worm_contents(contentsHtml):
    '''
    take html from contents and return a list of dicts with key of arc and child items of chapter URLs


    all chapters at in 1.01 or 1.x format, except epilogue and sequel teaser
    ''' 
    # chapter refs all seem to be nested in <div class="entry-content"> in the <article> tag 
    # so find all the href in tags that are descendents of <div class="entry-content">
    # divs don't seem to be included in .descendants. seems related to how html.parser parse the page.
    # lxml does OK.
    
    soup = BeautifulSoup(contentsHtml, 'lxml')
    chapterUrlParent = soup.find('div', 'entry-content')
    chapterUrls = [a['href'] for a in chapterUrlParent.find_all('a',href=not_contents)]
    return chapterUrls

def parse_worm_chapter(chapterHtml):
    '''
    take html from worm chapter, and turn just the story portion
    '''
    # story seems to be in <p> tags wrapped in <div class="entry-content">
    soup = BeautifulSoup(chapterHtml, 'lxml')
    storyParent = soup.find('div', 'entry-content')
    # destructive, but get rid of extra tags that hopefully aren't story text
    storyParent.find('div',id="jp-post-flair").decompose()
    for a in storyParent.find_all('a'): 
        a.decompose()
    return storyParent




https://parahumans.wordpress.com/2017/11/02/glow-worm-p-7/   
https://parahumans.wordpress.com/2017/11/04/glow-worm-p-8/        
https://parahumans.wordpress.com/2017/11/07/glow-worm-p-9/   
https://parahumans.wordpress.com/table-of-contents/?share=twitter
https://parahumans.wordpress.com/table-of-contents/?share=facebook