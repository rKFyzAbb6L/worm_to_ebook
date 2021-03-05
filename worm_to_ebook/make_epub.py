from ebooklib import epub
import re


# https://www.w3.org/publishing/epub32/epub-packages.html#sec-package-conformance-nav
# must have one package document
# must have must list all publication resources
# must have navigation document
# must have content document
#


def make_epub(chapter_list: list):
    '''
    epub is html, so just mash it up in there?
    '''

    book = epub.EpubBook()
    # required metadata
    book.set_identifier('Worm_3fd3da72-fe9c-43ae-8164-5309f2aae20c')
    book.set_title('Worm')
    book.set_language('en')
    book.add_author('John C. "Wildbow" McCrae')
    # should add link to source web serial here as well.
    # https://www.w3.org/publishing/epub32/epub-packages.html#sec-link-elem

    # generate a list of EpubHtml objects to use as chapters
    epub_chapters = list(map(make_epub_chapter, chapter_list))

    # add_item adds items into the EpubBook instance's manifest.
    # add_item returns the added item. This modifies the item in place. Like,
    # the reference is identical, but the item now has addition properties. The
    # book object instance's items property contains a list of items added.
    # This can be things other than our chapters though, so we want to keep
    # epub_chapters around
    list(map(book.add_item, epub_chapters))

    # collection element might be what i want for grouping each Arcs chapters
    # toc can have sections that group chapters
    book.toc = epub_chapters
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Spine element represents the default reading order
    # https://www.w3.org/publishing/epub32/epub-packages.html#sec-pkg-spine
    book.spine = ['nav'] + epub_chapters

    return book


def epub_toc_from_chapter_list(chapter_list):
    pass


def is_chapter_valid(chapter):
    return True


def make_epub_chapter(chapter):
    if not is_chapter_valid(chapter):
        raise Exception

    chapter_title = chapter['chapterTitle']
    chapter_file_name = clean_file_name(chapter['chapterTitle']) + ".html"
    chapter_content = chapter['chapterContent']

    # include chapter weblink in chaptermetadata
    epubChapter = epub.EpubHtml(title=chapter_title,
                                file_name=chapter_file_name,
                                content=chapter_content,
                                lang='en')

    return epubChapter


def clean_file_name(file_name_in):
    removechar = re.compile(r'[!@#$%\^&\*\(\)\[\]\{\}=\+<>\?:]')
    file_name_out = removechar.sub('', file_name_in.lower()).replace(' ', '_')
    return file_name_out

# {'chapterTitle': str(entry['title']),
#  'chapterUrl': str(chapter_url),
#  'chapterContent': entry['content'].prettify(formatter='html'),
#  'nextChapter': str(next_chapter),
#  'prevChapter': str(prev_chapter)}
