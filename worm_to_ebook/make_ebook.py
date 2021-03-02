from ebooklib import epub


def make_you_epub(book_dict: dict):
    '''
    epub is html, so just mash it up in there?
    '''

    book = epub.EpubBook()
    # i guess theres required metadata
    book.set_identifier('Worm_3fd3da72-fe9c-43ae-8164-5309f2aae20c')
    book.set_title('Worm')
    book.set_language('en')
    book.add_author('John C. "Wildbow" McCrae')

    for chapter in book_dict.keys():
        epubChapter = epub.EpubHtml(title=f"{arc.title}: {chapter.num}",
                                    file_name=f"{arc.title}.html",
                                    lang='en')
        epubChapter.set_content(chapter.content)
        book.add_item(epubChapter)
